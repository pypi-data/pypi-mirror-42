from triage.component.architect.feature_block import FeatureBlock


class SimpleQueryFeature(FeatureBlock):
    def __init__(self, query, *args, **kwargs):
        self.query = query
        super().__init__(*args, **kwargs)

    @property
    def final_feature_table_name(self):
        return f"{self.features_schema_name}.mytable"

    @property
    def feature_columns(self):
        return ['myfeature']

    @property
    def preinsert_queries(self):
        return [f"create table {self.final_feature_table_name}" "(entity_id bigint, as_of_date timestamp, myfeature float)"]

    @property
    def insert_queries(self):
        if self.features_ignore_cohort:
            final_query = self.query
        else:
            final_query = f"""
                select * from (self.query) raw
                join {self.cohort_table} using (entity_id, as_of_date)
            """
        return [
            final_query.format(as_of_date=date)
            for date in self.as_of_dates
        ]

    @property
    def postinsert_queries(self):
        return [f"create index on {self.final_feature_table_name} (entity_id, as_of_date)"]

    @property
    def imputation_queries(self):
        return [f"update {self.final_feature_table_name} set myfeature = 0.0 where myfeature is null"]

    def verify_no_nulls(self):
        if any(self.db_engine.execute(f"select 1 from {self.final_feature_table_name} where myfeature is null")):
            raise ValueError("Found nulls")

feature_block = SimpleQueryFeature(
    query="select entity_id, as_of_date, quantity from source_table where date < '{as_of_date}' limit 1",
    db_engine=<...>,

