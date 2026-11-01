import time
from core.emulator.coreemu import CoreEmu
from core.emulator.enumerations import EventTypes
from core.nodes.network import SwitchNode
from core.nodes.docker import DockerNode
from core.nodes.base import CoreNode, Position
from core.emulator.data import IpPrefixes, LinkOptions # Fix 1: Correct location of LinkOptions

# Helper tool to generate IP subnets for our interfaces
ip_prefixes = IpPrefixes(ip4_prefix="10.0.0.0/24")

# Initialize the emulator instance
coreemu = CoreEmu()
session = coreemu.create_session()

# Set to configuration state to add nodes and links
session.set_state(EventTypes.CONFIGURATION_STATE)

# Fix 3 & 5: Set specific model option for CoreNode and provide explicit Positions
router_options = CoreNode.create_options()
router_options.model = "router"

controller = session.add_node(CoreNode, position=Position(x=100, y=50), options=router_options)
n1 = session.add_node(DockerNode, position=Position(x=50, y=200))
n2 = session.add_node(DockerNode, position=Position(x=150, y=200))
n3 = session.add_node(DockerNode, position=Position(x=250, y=200))
s1 = session.add_node(SwitchNode, position=Position(x=150, y=350))

# Fix 4: Create virtual interface assignments for our L3 nodes
iface_n1 = ip_prefixes.create_iface(n1)
iface_n2 = ip_prefixes.create_iface(n2)
iface_n3 = ip_prefixes.create_iface(n3)

# Connect hosts to switch (Pass interface for host, None for switch)
session.add_link(n1.id, s1.id, iface_n1, None)
session.add_link(n2.id, s1.id, iface_n2, None)

# Connect n3 to s1 with impairment configurations
link_options = LinkOptions(
    delay=100000,  # Note: CORE LinkOptions delay is measured in microseconds (100ms = 100000)
    loss=2         # Percentage
)
session.add_link(n3.id, s1.id, interface_one=iface_n3, options=link_options)

# Fix 2: Start the simulation session
session.instantiate()

print("Topology successfully deployed! Keeping script alive for 60 seconds...")
try:
    time.sleep(60)
finally:
    # Always gracefully shut down to clean up virtual interfaces & network namespaces
    session.shutdown()
