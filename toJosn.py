class JSONHelper():
    @staticmethod
    def to_json_list(target_list):
        result = []
        for item in target_list:
            jsondata = {}
            for k, v in vars(item).items():
                print(k)
                if k != '_sa_instance_state':
                    tdic={
                        k: v
                    }
                    jsondata.update(tdic)
            result.append(jsondata)
        print(result)
        return result
        
    