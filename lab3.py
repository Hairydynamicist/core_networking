"""
creating a basic three-node/one-switch topology using the pythonAPI
"""
from core import Session
from core.nodes import SwitchNode, CtrlNode
from core.nodes import DockerNode
from core.link import LinkOptions

# create a session
session = Session()

# Add a controller
controller = session.add_node(CtrlNode)

# Add in three hosts (PC nodes)
n1 = session.add_node(DockerNode, name="n1")
n2 = session.add_node(DockerNode, name="n2")
n3 = session.add_node(DockerNode, name="n3")

# Add a switch
s1 = session.add_node(SwitchNode, name="s1")

# Connect hosts to switch
session.add_link(n1,s1)
session.add_link(n2,s1)

# Connect n3 to s1 with impairment
link_options = LinkOptions()
link_options.delay = 100 # milliseconds
link_options.loss = 2 # percent
session.add_link(n3, s1, link_options=link_options)

# Start the session
session.start()

# Keep it running
print("Emulation running. Press Ctrl+c to stop.")
try:
    while True:
        pass
except KeyboardInterrupt:
    pass
finally:
    # Clean up
    session.stop()