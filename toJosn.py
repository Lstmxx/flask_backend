class JSONHelper():
    @staticmethod
    def to_json(item):
        jsondata = {}
        for k, v in vars(item).items():
            if k != '_sa_instance_state':
                tdic = {
                    k: v
                }
                jsondata.update(tdic)
        return jsondata
    @staticmethod
    def to_json_list(target_list):
        result = []
        for item in target_list:
            jsondata = JSONHelper.to_json(item)
            result.append(jsondata)
        print(result)
        return result
        
    