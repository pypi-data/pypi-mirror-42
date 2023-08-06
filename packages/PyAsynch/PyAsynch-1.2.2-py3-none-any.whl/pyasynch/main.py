# IMPORTS
import logging
from pyasynch.environment import Environment

# ======================
# Startup
# ======================

logger = logging.getLogger(__name__)
env = Environment()

# ==================
# Registering nodes
# ==================
# env.register_node('auth',Auth(env.endpoint))


# ====
# RUN
# ====
try:
    env.run()
except KeyboardInterrupt:
    env.stop()
