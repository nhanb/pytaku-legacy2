import sys
import os

# Add project root to PATH
test_path = os.path.dirname(__file__)
sys.path.append(os.path.dirname(test_path))

# Add google app engine SDK to PATH
gae_path = os.environ.get('GAE_PATH')
sys.path.append(gae_path)
