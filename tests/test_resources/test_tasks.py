from invoke.context import Context


def test_resources_validate_task(plugins_discovered):
    from handmade.resources.tasks import validate
    validate(Context())


def test_resources_list_resources():
    raise NotImplementedError()