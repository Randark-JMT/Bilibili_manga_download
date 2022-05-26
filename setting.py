import json

setting_file = "setting.json"
properties_global = {}


def settintfile_read():
    """
    读取设置文件所有内容
    """
    f = open(setting_file, 'r')
    json_text = f.read()
    f.close()
    return json_text


def settingfile_write(json_text):
    """
    所有内容覆盖到设置文件中。
    """
    try:
        f = open(setting_file, 'w')
        f.write(json_text)
        f.close()
        return True
    except Exception:
        return False


def property_put(key, value, properties, domain=None):
    """
    保存一个属性。如果key不存在，则创建；存在，则覆盖。
    """
    properties[domain][key] = value
    json_text = json.dumps(properties)
    settingfile_write(json_text)
    return properties


def property_get(key, properties, default=None, domain=None):
    """
    获取一个属性。如果不存在，则返回default。
    """
    if key in properties[domain]:
        return properties[domain][key]
    else:
        return default
