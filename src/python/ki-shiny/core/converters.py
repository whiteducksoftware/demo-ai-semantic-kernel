from typing import List

import pandas as pd


class Converters:
    @staticmethod
    def convert_objectlist_to_dataframe(objects_list: List[object]) -> pd.DataFrame:
        data = [obj.__dict__ for obj in objects_list]

        # Create DataFrame from list of dictionaries
        df = pd.DataFrame(data)

        return df
