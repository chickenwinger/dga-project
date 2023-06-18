from flask import current_app
import pandas as pd
import json
from dga import db
from dga.rtdatabase import get_current_user

def create_dataframe():
    with current_app.app_context():
        user = get_current_user()

        all_records = db.child("records").child(user["localId"]).get()

        transformer_list = []
        timestamp_list = []
        fault_type_list = []
        record_tag_list = []
        gaseous_list = []

        # [TX1, TX2, TX3, TX4, TX5]
        for record in all_records.each():
            inner_record = (
                db.child("records").child(user["localId"]).child(record.key()).get()
            )

            if inner_record.each() is not None:
                for data in inner_record.each():
                    transformer_list.append(record.key())
                    print(transformer_list)
                    record_tag_list.append(data.key())

                    timestamp = pd.to_datetime(data.val()["timestamp"], unit="s")
                    print(timestamp)
                    timestamp_list.append(timestamp)

                    fault_type = [
                        data.val()["fault_type"].get(tool)
                        for tool in data.val()["fault_type"]
                    ]
                    fault_type_list.append(fault_type)

                    gaseous = [
                        data.val()["gaseous_data"].get(gas)
                        for gas in data.val()["gaseous_data"]
                    ]
                    gaseous_list.append(gaseous)

        df = pd.DataFrame(
            {
                "transformerList": all_records,
                "transformerKey": transformer_list,
                "Record": record_tag_list,
                "Acetylene": [gas[0] for gas in gaseous_list],
                "Carbon dioxide": [gas[1] for gas in gaseous_list],
                "Carbon monoxide": [gas[2] for gas in gaseous_list],
                "Ethane": [gas[3] for gas in gaseous_list],
                "Ethylene": [gas[4] for gas in gaseous_list],
                "Hydrogen": [gas[5] for gas in gaseous_list],
                "Methane": [gas[6] for gas in gaseous_list],
            }
        )

        print(df)

        return df
