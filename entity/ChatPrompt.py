import json

from common.JsonObj import JsonObj


class ChatPrompt(JsonObj):
    def __init__(self, id, prompt, target, prompt_delete_reason, target_delete_reason, create_time,
                 update_time, delete_time):
        self.id = id
        self.prompt = prompt
        self.target = target
        self.prompt_delete_reason = prompt_delete_reason
        self.target_delete_reason = target_delete_reason
        self.create_time = create_time
        self.update_time = update_time
        self.delete_time = delete_time


def __str__(self):
    return json.dumps(self.__dict__)


def __repr__(self):
    return self.__str__()


def to_json(self):
    return self.__str__()


def json(self):
    return self.__str__()
