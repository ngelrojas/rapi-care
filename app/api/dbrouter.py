def decide_on_model(model):
    return "flow_data" if model._meta.app_label == "flow_data" else None


class FlowDbRouter:
    """
    Implements a database router so that:
    * Django related data - DB alias `default`
    * Flow Backend database data (everything "non-Django") - DB alias `core`
    """

    def db_for_read(self, model, **hints):
        return decide_on_model(model)

    def db_for_write(self, model, **hints):
        return decide_on_model(model)

    def allow_relation(self, obj1, obj2, **hints):
        # Allow any relation if both models are part of the flowdata app
        if obj1._meta.app_label == "flow_data" and obj2._meta.app_label == "flow_data":
            return True
        # Allow if neither is part of flowdata app
        elif "flow_data" not in [obj1._meta.app_label, obj2._meta.app_label]:
            return True
        # by default return None - "undecided"

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # allow migrations on the "default" (django related data) DB
        if db == "default" and app_label != "flow_data":
            return True

        # allow migrations on the legacy database too:
        # this will enable to actually alter the database schema of the legacy DB!
        # if db == 'flow_data' and app_label == "flowdata":
        # return True

        return False
