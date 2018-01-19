""" Config for Demo Location """

country_config = {
    "country_name": "Demo",
    "authentication_token": "",
    "tables": [
        "demo_case",
        "demo_alert",
        "demo_register",
        "jor_evaluation",
        "dem_test",
        "rms_test"
    ],
    "scramble_fields": {
        "dem_evaluation": ["simid", "phonenumber"]
    },
    "hash_fields": {
        "demo_case": ["pt1:gender"]
    },
    "patient_id": {
        "demo_case": {
            "field_name": 'pt:pid',
            "validation": "^[1234567890]{10,10}$",
            "translate": True,
            "exclude": [1234567890, 1111111111]
        }
    },
    "rename_fields": {
        "demo_case": {'*meta-instance-id*': 'meta/instanceID',
                      '*meta-submission-date*': 'SubmissionDate',
                      "visit_date": "pt./visit_date",
                      "gender": "pt1./gender",
                      "age": "pt1./age",
                      "visit": "intro./visit"
                      },
        "demo_alert": {'*meta-instance-id*': 'meta/instanceID',
                       '*meta-submission-date*': 'SubmissionDate'},
        "demo_register": {'*meta-instance-id*': 'meta/instanceID',
                          '*meta-submission-date*': 'SubmissionDate'},
        "dem_test": {'*meta-instance-id*': 'meta/instanceID',
                     '*meta-submission-date*': 'SubmissionDate'},
    },
    "rename_forms": {
        "dem_test": "demo_testing"
    },
    "replace_characters": {
        "demo_case":
            [[":", "./"]]
    },
    "supported_content":
        {
            "form": {
                "token": "",
                "content": "",
                "formId": "",
                "formVersion": "",
                "data": ""
            },
            "record": {
                "token": "",
                "content": "",
                "formId": "",
                "formVersion": "",
                "data": ""
            }
        }
}
