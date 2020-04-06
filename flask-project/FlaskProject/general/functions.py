from uuid import UUID
import datetime


def obj_to_dict(row):
    from datetime import datetime as dt, date as d
    if row is None:
        return None
    dicts = {}
    for column in row.__table__.columns:

        if type(getattr(row, column.name)) is d:
            dicts[column.name] = datetime.datetime.strftime(
                getattr(row, column.name), "%Y-%m-%d")

        elif type(getattr(row, column.name)) is dt:
            dicts[column.name] = datetime.datetime.strftime(
                getattr(row, column.name), "%Y-%m-%d %H:%M:%S")

        elif type(getattr(row, column.name)) is UUID:
            dicts[column.name] = str(getattr(row, column.name))

        else:
            dicts[column.name] = getattr(row, column.name)

    return dicts


def obj_to_dict_complex_query(row):
    from datetime import datetime as dt, date as d
    dicts = dict()
    for field_name in row._fields:
        dict_object = dict()
        if getattr(row, field_name) is not None:
            for column in getattr(row, field_name).__table__.columns:

                if type(getattr(getattr(row, field_name), column.name)) is d:
                    dict_object[column.name] = datetime.datetime.strftime(
                        getattr(getattr(row, field_name), column.name),
                        "%Y-%m-%d")

                elif type(getattr(getattr(row, field_name), column.name)) is dt:
                    dict_object[column.name] = datetime.datetime.strftime(
                        getattr(getattr(row, field_name), column.name),
                        "%Y-%m-%d %H:%M:%S")

                elif type(getattr(getattr(row, field_name), column.name)) \
                        is UUID:
                    dict_object[column.name] = str(getattr(getattr(
                        row, field_name), column.name))

                else:
                    dict_object[column.name] = getattr(getattr(row, field_name),
                                                       column.name)

        dicts[getattr(row, field_name).__table__.name] = dict_object \
            if dict_object else None

    return dicts












