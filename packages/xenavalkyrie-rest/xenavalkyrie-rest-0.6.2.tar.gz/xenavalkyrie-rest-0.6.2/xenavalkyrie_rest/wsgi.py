from xenavalkyrie_rest.namespaces.base_ns import app

# Build namespaces.
from xenavalkyrie_rest.namespaces.session_ns import session_ns
from xenavalkyrie_rest.namespaces.chassis_ns import chassis_ns
from xenavalkyrie_rest.namespaces.module_ns import module_ns
from xenavalkyrie_rest.namespaces.port_ns import port_ns
from xenavalkyrie_rest.namespaces.stream_ns import stream_ns
from xenavalkyrie_rest.namespaces.modifier_ns import modifier_ns, xmodifier_ns
from xenavalkyrie_rest.namespaces.capture_ns import capture_ns
from xenavalkyrie_rest.namespaces.server_ns import management_ns

if __name__ == "__main__":
    app.run()
