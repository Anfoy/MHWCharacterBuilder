class Item:
    def __init__(self, name, id, skill, level):
        self.name = name
        self.id = id
        self.skill = skill
        self.level = level

    @classmethod
    def from_json(cls, json_data):
        if 'name' not in json_data or 'id' not in json_data:
            return None
        skill_info = None
        skill_level = 0
        if 'skills' in json_data and json_data['skills']:
            first_skill = json_data['skills'][0]
            if 'skill' in first_skill and 'name' in first_skill['skill']:
                skill_info = first_skill['skill']['name']
            if 'level' in first_skill:
                skill_level = first_skill['level']
        return cls(
            name=json_data['name'],
            id=json_data['id'],
            skill=skill_info,
            level=skill_level
        )

    def __str__(self):
        return self.name + ", " + str(self.id) + ", " + str(self.skill) + ", " + str(self.level)