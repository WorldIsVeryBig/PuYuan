from django import forms
from django.core.validators import RegexValidator

class PersonalDefaultForm(forms.Form):
    sugar_delta_max = forms.DecimalField(max_digits=5,
                                         decimal_places=0,
                                         required=False)
    sugar_delta_min = forms.DecimalField(max_digits=5,
                                         decimal_places=0,
                                         required=False)
    sugar_morning_max = forms.DecimalField(max_digits=5,
                                           decimal_places=0,
                                           required=False)
    sugar_morning_min = forms.DecimalField(max_digits=5,
                                           decimal_places=0,
                                           required=False)
    sugar_evening_max = forms.DecimalField(max_digits=5,
                                           decimal_places=0,
                                           required=False)
    sugar_evening_min = forms.DecimalField(max_digits=5,
                                           decimal_places=0,
                                           required=False)
    sugar_before_max = forms.DecimalField(max_digits=5,
                                          decimal_places=0,
                                          required=False)
    sugar_before_min = forms.DecimalField(max_digits=5,
                                          decimal_places=0,
                                          required=False)
    sugar_after_max = forms.DecimalField(max_digits=5,
                                         decimal_places=0,
                                         required=False)
    sugar_after_min = forms.DecimalField(max_digits=5,
                                         decimal_places=0,
                                         required=False)
    systolic_max = forms.DecimalField(max_digits=5,
                                      decimal_places=0,
                                      required=False)
    systolic_min = forms.DecimalField(max_digits=5,
                                      decimal_places=0,
                                      required=False)
    diastolic_max = forms.DecimalField(max_digits=5,
                                       decimal_places=0,
                                       required=False)
    diastolic_min = forms.DecimalField(max_digits=5,
                                       decimal_places=0,
                                       required=False)
    pulse_max = forms.DecimalField(max_digits=5,
                                   decimal_places=0,
                                   required=False)
    pulse_min = forms.DecimalField(max_digits=5,
                                   decimal_places=0,
                                   required=False)
    weight_max = forms.DecimalField(max_digits=5,
                                    decimal_places=0,
                                    required=False)
    weight_min = forms.DecimalField(max_digits=5,
                                    decimal_places=0,
                                    required=False)
    bmi_max = forms.DecimalField(max_digits=5,
                                 decimal_places=0,
                                 required=False)
    bmi_min = forms.DecimalField(max_digits=5,
                                 decimal_places=0,
                                 required=False)
    body_fat_max = forms.DecimalField(max_digits=5,
                                      decimal_places=0,
                                      required=False)
    body_fat_min = forms.DecimalField(max_digits=5,
                                      decimal_places=0,
                                      required=False)