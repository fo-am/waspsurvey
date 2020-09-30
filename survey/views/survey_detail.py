# -*- coding: utf-8 -*-
import logging

import random
from django.conf import settings
from django.shortcuts import redirect, render, reverse
from django.views.generic import View

from survey.decorators import survey_available
from survey.forms import ResponseForm

from survey.models import Question, Answer, Insect

LOGGER = logging.getLogger(__name__)

class SurveyDetail(View):
    
    @survey_available
    def get(self, request, *args, **kwargs):
        survey = kwargs.get("survey")
        step = kwargs.get("step", 0)
        if survey.template is not None and len(survey.template) > 4:
            template_name = survey.template
        else:
            if survey.is_all_in_one_page():
                template_name = "survey/one_page_survey.html"
            else:
                template_name = "survey/survey.html"
        if survey.need_logged_user and not request.user.is_authenticated:
            return redirect("%s?next=%s" % (settings.LOGIN_URL, request.path))

        # create a random number to use for ordering for this session only
        if step==0 or "random" not in request.session:
            request.session["random"] = random.randrange(0,100000)

        form = ResponseForm(survey=survey,
                            user=request.user,
                            step=step,
                            seed=request.session["random"])
        
        categories = form.current_categories()

        # get insects by location
        insects = []
        location = ""
        try:
            q=Question.objects.get(code=Question.USER_LOCATION)            
            session_key = "survey_%s" % (kwargs["id"],)
            if session_key in request.session:
                question_id = "question_"+str(q.id)
                if question_id in request.session[session_key]:
                    location = request.session[session_key][question_id]                
                    insects = Insect.objects.filter(location=location)
        except Question.DoesNotExist:
            location="no location question"

        #  load known insects if they have been recorded yet
        known_insects = []
        try:
            q=Question.objects.get(code=Question.WASPS_KNOWN)            
            session_key = "survey_%s" % (kwargs["id"],)
            if session_key in request.session:
                question_id = "question_"+str(q.id)
                if question_id in request.session[session_key]:
                    i = request.session[session_key][question_id]                    
                    known_insects = Insect.objects.filter(name__in=i.split(","))
        except Question.DoesNotExist:
            pass

            
        asset_context = {
            # If any of the widgets of the current form has a "date" class, flatpickr will be loaded into the template
            "flatpickr": any([field.widget.attrs.get("class") == "date" for _, field in form.fields.items()])
        }
        context = {
            "response_form": form,
            "survey": survey,
            "categories": categories,
            "step": step,
            "asset_context": asset_context,
            "location": location,
            "insects": insects,
            "known_insects": known_insects
        }

        return render(request, template_name, context)

    @survey_available
    def post(self, request, *args, **kwargs):
        survey = kwargs.get("survey")
        if survey.need_logged_user and not request.user.is_authenticated:
            return redirect("%s?next=%s" % (settings.LOGIN_URL, request.path))

        form = ResponseForm(request.POST, survey=survey, user=request.user, step=kwargs.get("step", 0))
        categories = form.current_categories()

        if not survey.editable_answers and form.response is not None:
            LOGGER.info("Redirects to survey list after trying to edit non editable answer.")
            return redirect(reverse("survey-list"))
        context = {"response_form": form, "survey": survey, "categories": categories}
        if form.is_valid():
            return self.treat_valid_form(form, kwargs, request, survey)
        return self.handle_invalid_form(context, form, request, survey)

    @staticmethod
    def handle_invalid_form(context, form, request, survey):
        LOGGER.info("Non valid form: <%s>", form)
        if survey.template is not None and len(survey.template) > 4:
            template_name = survey.template
        else:
            if survey.is_all_in_one_page():
                template_name = "survey/one_page_survey.html"
            else:
                template_name = "survey/survey.html"
        return render(request, template_name, context)

    def treat_valid_form(self, form, kwargs, request, survey):
        session_key = "survey_%s" % (kwargs["id"],)
        if session_key not in request.session:
            request.session[session_key] = {}
        for key, value in list(form.cleaned_data.items()):
            request.session[session_key][key] = value
            request.session.modified = True
        next_url = form.next_step_url()
        response = None
        if survey.is_all_in_one_page():
            response = form.save()
        else:
            # when it's the last step
            if not form.has_next_step():
                save_form = ResponseForm(request.session[session_key], survey=survey, user=request.user)
                if save_form.is_valid():
                    response = save_form.save()
                else:
                    LOGGER.warning("A step of the multipage form failed but should have been discovered before.")
        # if there is a next step
        if next_url is not None:
            return redirect(next_url)
        del request.session[session_key]
        if response is None:
            return redirect(reverse("survey-list"))
        next_ = request.session.get("next", None)
        if next_ is not None:
            if "next" in request.session:
                del request.session["next"]
            return redirect(next_)
        return redirect("survey-confirmation", uuid=response.interview_uuid)
