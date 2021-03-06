from pathlib import Path
import pandas as pd
from django.core.management.base import BaseCommand
from findstore import settings
from api import models


class Command(BaseCommand):
    help = "initialize database"
    DATA_DIR = Path(settings.BASE_DIR).parent / "data"
    DATA_FILE = str(DATA_DIR / "card_data.pkl")

    def _load_dataframes(self):
        try:
            data = pd.read_pickle(Command.DATA_FILE)
        except:
            print(f"[-] Reading {Command.DATA_FILE} failed")
            exit(1)
        return data

    def _initialize(self):
        """
        Sub PJT 1에서 만든 Dataframe을 이용하여 DB를 초기화합니다.
        """
        print("[*] Loading data...")
        dataframes = self._load_dataframes()

        print("[*] Initializing stores...")
        models.CardData.objects.all().delete()
        
        carddatas_bulk = [
            models.CardData(
                sex=carddata.sex,
                avg_age=carddata.avg_age,
                time=carddata.time,
                dong=carddata.dong,
                ppl=carddata.ppl,
                cnt=carddata.cnt
            )
            for carddata in dataframes.itertuples()
        ]
        models.CardData.objects.bulk_create(carddatas_bulk)

        print("[+] Done")

    def handle(self, *args, **kwargs):
        self._initialize()