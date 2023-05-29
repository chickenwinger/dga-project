from flask import current_app
import pandas as pd

from dga import db
from dga.rtdatabase import get_current_user


def create_dataframe():
    with current_app.app_context():
        user = get_current_user()

        all_records = db.child("records").child(user["localId"]).get()

        timestamp_list = []
        fault_type_list = []
        record_tag_list = []

        for record in all_records.each():
            record_tag_list.append(record.key())

            timestamp = pd.to_datetime(record.val()["timestamp"], unit="s")
            timestamp_list.append(timestamp)

            fault_type = [
                record.val()["fault_type"].get(tool)
                for tool in record.val()["fault_type"]
            ]
            fault_type_list.append(fault_type)

        df = pd.DataFrame(
            {
                "Record": record_tag_list,
                "Timestamp": timestamp_list,
                "Fault Type (dt1)": [fault[0] for fault in fault_type_list],
                "Fault Type (dt4)": [fault[1] for fault in fault_type_list],
                "Fault Type (dt5)": [fault[2] for fault in fault_type_list],
            }
        )

        print(df)

        return df
