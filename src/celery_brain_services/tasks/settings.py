from category_encoders import BinaryEncoder, OrdinalEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

from brain_services.transformers import (
    CleanNanValuesTransformer, DataFrameColumnNamesTransformer, DateTimeTransformer, DropUnnecessaryDataTransformer,
    ExtractDateTimeInfoTransformer, ExtractDaysBetweenDatesTransformer, RemoveColumnNegativeValuesTransformer,
    SwapInvalidDatesTransformer,
)

NAMES_TO_UPDATE_LIST = [
    ('gender', 'Gender'),
    ('handicap', 'Handcap'),
    ('scheduled_day', 'ScheduledDay'),
    ('appointment_day', 'AppointmentDay'),
    ('hypertension', 'Hipertension'),
    ('age', 'Age'),
    ('scholarship', 'Scholarship'),
    ('diabetes', 'Diabetes'),
    ('alcoholism', 'Alcoholism'),
    ('sms_received', 'SMS_received'),
    ('neighbourhood', 'Neighbourhood'),
]
MODELS_TO_USE_LIST = [
    ('decision_tree', DecisionTreeClassifier()),
    ('naive_bayes_gaussian', GaussianNB()),
    ('knn', KNeighborsClassifier()),
    ('random_forest', RandomForestClassifier()),
]
BASE_STEPS = [
    ('drop_unnecessary_data', DropUnnecessaryDataTransformer(unnecessary_columns=['PatientId', 'AppointmentID'])),
    ('column_names_transformer', DataFrameColumnNamesTransformer(names_to_update_list=NAMES_TO_UPDATE_LIST)),
    ('binary_encoder', BinaryEncoder(cols=['gender', ])),
    ('transform_neighbourhood', OrdinalEncoder(cols=['neighbourhood', ])),
    # (
    #     # This transformer has some problems due the small amount of data
    #     'transform_neighbourhood', NeighbourhoodTransformer()
    # ),
    (
        'transform_scheduled_day',
        DateTimeTransformer(column_name='scheduled_day', format_to_use='%Y-%m-%dT%H:%M:%SZ')
    ),
    ('transform_appointment_day', DateTimeTransformer(column_name='appointment_day', format_to_use='%Y-%m-%dT')),
    (
        'appointment_day_of_week',
        ExtractDateTimeInfoTransformer(
            base_column_name='appointment_day',
            final_column_name='day_of_week_of_appointment',
            info_to_extract='day_of_week',
        )
    ),
    (
        'scheduled_day_of_week',
        ExtractDateTimeInfoTransformer(
            base_column_name='scheduled_day',
            final_column_name='day_of_week_of_scheduled',
            info_to_extract='day_of_week',
        )
    ),
    (
        'scheduled_hour',
        ExtractDateTimeInfoTransformer(
            base_column_name='scheduled_day',
            final_column_name='hour_of_scheduled',
            info_to_extract='hour',
        )
    ),
    (
        'appointment_day',
        ExtractDateTimeInfoTransformer(
            base_column_name='appointment_day',
            final_column_name='day_of_appointment',
            info_to_extract='day',
        )
    ),
    (
        'scheduled_day',
        ExtractDateTimeInfoTransformer(
            base_column_name='scheduled_day',
            final_column_name='day_of_scheduled',
            info_to_extract='day',
        )
    ),
    (
        'appointment_date',
        ExtractDateTimeInfoTransformer(
            base_column_name='appointment_day',
            final_column_name='date_of_appointment',
            info_to_extract='date',
        )
    ),
    (
        'scheduled_date',
        ExtractDateTimeInfoTransformer(
            base_column_name='scheduled_day',
            final_column_name='date_of_scheduled',
            info_to_extract='date',
        )
    ),
    (
        'appointment_month',
        ExtractDateTimeInfoTransformer(
            base_column_name='appointment_day',
            final_column_name='month_of_appointment',
            info_to_extract='month',
        )
    ),
    (
        'scheduled_month',
        ExtractDateTimeInfoTransformer(
            base_column_name='scheduled_day',
            final_column_name='month_of_scheduled',
            info_to_extract='month',
        )
    ),
    (
        'clean_invalid_dates',
        SwapInvalidDatesTransformer(
            greater_date_column_name='date_of_appointment',
            lower_date_column_name='date_of_scheduled',
        )
    ),

    (
        'extract_days_between',
        ExtractDaysBetweenDatesTransformer(
            final_column_name='days_between_scheduled_and_appointment',
            greater_date_column_name='date_of_appointment',
            lower_date_column_name='date_of_scheduled',
        )
    ),
    (
        'drop_unnecessary_datetime_data',
        DropUnnecessaryDataTransformer(
            unnecessary_columns=[
                'appointment_day', 'scheduled_day', 'date_of_appointment', 'date_of_scheduled', 'neighbourhood'
            ]
        )
    ),
    ('remove_column_negatives', RemoveColumnNegativeValuesTransformer(column_name='age')),
    ('clean_nan_values', CleanNanValuesTransformer()),
]
PCA_OPTIMIZATION_COMPONENTS = [False, 16, 8, 4, 2]  # From higher resources to lower
