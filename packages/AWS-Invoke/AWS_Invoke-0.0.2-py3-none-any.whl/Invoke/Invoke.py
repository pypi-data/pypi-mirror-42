import boto3
import json
import inspect


FUNCTION_CONTEXT = None
HANDLER = None
INVOKE_LOCAL = None


class Link_Invocation(object):
    def get_args_from(self, target):
        spec = inspect.getargspec(target)
        return spec.args, spec.args[:-len(spec.defaults) if spec.defaults else None]

    def get_optional_args_from(self, target):
        spec = inspect.getargspec(target)
        return spec.args[-len(spec.defaults):] if spec.defaults else []

    def __init__(self,
                 target):
        self.target = target
        self.all_arguments, self.required_arguments = self.get_args_from(target)

    def legal_event(self, event):
        contains_required_args = set(self.required_arguments) <= set(event)
        no_unrecognized_args = set(event) <= set(self.all_arguments)

        return contains_required_args and no_unrecognized_args

    def handler_decorator(self, handler):
        def wrapped_handler(event, context):
            global FUNCTION_CONTEXT
            FUNCTION_CONTEXT = context
            handler_result = handler(event, context)

            if self.legal_event(event):
                return self.target(**event)
            else:
                return handler_result

        return wrapped_handler

    def __call__(self, handler):
        return self.handler_decorator(handler)


class DummyContext():
    def __init__(self, name="DummyContext", invoke_local=True, **kwargs):
        self.function_name = name
        self.invoke_local = invoke_local
        for kw in kwargs:
            setattr(self, kw, kwargs[kw])


def Invoke(event):
    global INVOKE_LOCAL
    global HANDLER

    if INVOKE_LOCAL:
        HANDLER(event, FUNCTION_CONTEXT)
    else:
        resp = boto3.client('lambda').invoke(FunctionName=FUNCTION_CONTEXT.function_name,
                                             InvocationType="Event",
                                             Payload=json.dumps(event).encode('utf-8'))

        if not 200 <= resp['StatusCode'] < 300:
            raise Exception("Unable to invoke function %s" % FUNCTION_CONTEXT.function_name)


def Initialize_Invoker(context, handler):
    global FUNCTION_CONTEXT
    global HANDLER
    global INVOKE_LOCAL

    FUNCTION_CONTEXT = context
    HANDLER = handler
    try:
        INVOKE_LOCAL = context.invoke_local
    except Exception:
        pass


if __name__ == "__main__":
    def wrapper(test):
        print(test)

    @Link_Invocation(wrapper)
    def test_handler(event, context):
        Initialize_Invoker(context, test_handler)

    event = {"test": "It's working!"}
    context = DummyContext("Invoke")
    test_handler(event, context)

