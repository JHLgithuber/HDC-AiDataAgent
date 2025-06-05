from openai import OpenAI
from dotenv import load_dotenv
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionFunctionCallOptionParam
import os
import sys
import json


class IsContainDataset:
    def __init__(self, keyword, model_name="gpt-4.1-nano", model_temp=1.1,):
        self.keyword = keyword
        load_dotenv()
        self.dataset_classes_json = dict()
        self.load_dataset_classes_list("dataset_classes.json")

        self.dataset_names = list(self.dataset_classes_json.keys())
        self.openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model_name = model_name
        self.model_temp = model_temp

    def load_dataset_classes_list(self, dataset_path):
        with open(dataset_path, "r", encoding="utf-8") as f:
            self.dataset_classes_json = json.load(f)

    def request_dataset_by_openai(self):
        """
        시스템 메시지만으로 교통사고 영상 검색에 쓸 수 있는
        최대한 많은 키워드를 max_keywords 개수만큼 생성하여 리스트로 반환합니다.
        """
        # 1) 함수 스펙 정의
        functions = [
            {
                "name": "extract_dataset_classes",
                "description": "사용자가 요구하는 키워드가 데이터셋에 포함되어 있는지 판단",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "is_contain": {
                            "type": "boolean",
                            "description": "데이터셋에 포함되어 있으면 true, 없으면 false"
                        },
                        "what_dataset":{
                            "type": "string",
                            "description": "포함되어있는 DataSet 명, 없으면 None"
                        },
                        "what_id": {
                            "type": "integer",
                            "description": "해당되는 DataSet Class의 ID, 없으면 -1"
                        }
                    },
                    "required": ["is_contain", "what_dataset", "what_id"]
                }
            },
            {
                "name": "search_dataset_classes",
                "description": "Dataset과 이름, id를 검색",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "search_keyword": {
                            "type": "string",
                            "description": f"{self.dataset_names}에서 키워드를 검색하여 리턴"
                        }
                    },
                    "required": ["search_keyword"]
                }
            },

        ]

        response = self.openai.chat.completions.create(
            model=self.model_name,
            messages=[
                ChatCompletionSystemMessageParam(
                    role="system",
                    content=f"사용자가 입력한 키워드는 다음과 같다: {self.keyword}"
                            f"위 키워드를 DataSet에 펑션콜을 통해 조회하여 나온 결과를 바탕으로 결정할것"
                            f"적절한 펑션콜로만 응답할것"
                )
            ],
            functions=functions,
            function_call="auto",
            temperature=self.model_temp,
            timeout=60
        )


        msg = response.choices[0].message.function_call.arguments
        print("Row_return" + msg)  # 실제 값 확인
        json_args = json.loads(msg)


        if json_args.get("is_contain", None) is not None:
            return json_args.get("is_contain", None), json_args.get("what_dataset", None), json_args.get("what_id", None)
        elif json_args.get("search_keyword", None) is not None:
            pass
        else:
            pass

    #TODO: 검색 메서드 추가


# -- 사용 예시 --
if __name__ == "__main__":
    is_contain = IsContainDataset(keyword="자동차")

    #is_contain.request_dataset_by_openai()
    print(is_contain.request_dataset_by_openai())


