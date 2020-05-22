#!/usr/bin/python

##############################################################################################
# Copyright (C) 2020 Carmine Scarpitta - (Consortium GARR and University of Rome 'Tor Vergata')
# www.garr.it - www.uniroma2.it/netgroup
#
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Example showing how it is possible to switch from a SRv6 
# tunnel to another by acting on the metric parameter
#
# @author Carmine Scarpitta <carmine.scarpitta@uniroma2.it>
#

import os

# Activate virtual environment if a venv path has been specified in .venv
# This must be executed only if this file has been executed as a 
# script (instead of a module)
if __name__ == '__main__':
    # Check if .venv file exists
    if os.path.exists('.venv'):
        with open('.venv', 'r') as venv_file:
            # Get virtualenv path from .venv file
            venv_path = venv_file.read()
        # Get path of the activation script
        venv_path = os.path.join(venv_path, 'bin/activate_this.py')
        if not os.path.exists(venv_path):
            print('Virtual environment path specified in .venv '
                  'points to an invalid path\n')
            exit(-2)
        with open(venv_path) as f:
            # Read the activation script
            code = compile(f.read(), venv_path, 'exec')
            # Execute the activation script to activate the venv
            exec(code, {'__file__': venv_path})

# Imports
import sys
import logging
import time
from threading import Thread
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Folder containing this script
BASE_PATH = os.path.dirname(os.path.realpath(__file__))

# Folder containing the controller
CONTROLLER_PATH = os.path.join(BASE_PATH, '../controller/')

# Environment variables have priority over hardcoded paths
# If an environment variable is set, we must use it instead of
# the hardcoded constant

# CONTROLLER_PATH
if os.getenv('CONTROLLER_PATH') is not None:
    # Check if the CONTROLLER_PATH variable is set
    if os.getenv('CONTROLLER_PATH') == '':
        print('Error : Set CONTROLLER_PATH variable in .env\n')
        sys.exit(-2)
    # Check if the CONTROLLER_PATH variable points to an existing folder
    if not os.path.exists(CONTROLLER_PATH):
        print('Error : CONTROLLER_PATH variable in '
              '.env points to a non existing folder')
        sys.exit(-2)
    # CONTROLLER_PATH in .env is correct. We use it.
    CONTROLLER_PATH = os.getenv('CONTROLLER_PATH')
else:
    # CONTROLLER_PATH in .env is not set, we use the hardcoded path
    #
    # Check if the CONTROLLER_PATH variable is set
    if CONTROLLER_PATH == '':
        print('Error : Set CONTROLLER_PATH variable in .env or %s' % sys.argv[0])
        sys.exit(-2)
    # Check if the CONTROLLER_PATH variable points to an existing folder
    if not os.path.exists(CONTROLLER_PATH):
        print('Error : CONTROLLER_PATH variable in '
              '%s points to a non existing folder' % sys.argv[0])
        print('Error : Set CONTROLLER_PATH variable in .env or %s\n' % sys.argv[0])
        sys.exit(-2)

# SRv6PM dependencies
sys.path.append(CONTROLLER_PATH)
import srv6_pm
import utils


# Global variables definition
#
#
# Logger reference
logging.basicConfig(level=logging.NOTSET)
logger = logging.getLogger(__name__)
#
# Port of the gRPC server
GRPC_PORT = 12345


def start_experiment():
    """Start a new experiment"""

    logger.info('*** Starting a new experiment')
    # IP addresses
    sender = 'fcfd:0:0:1::1'
    reflector = 'fcfd:0:0:8::1'
    logger.info('Sender: %s' % sender)
    logger.info('Reflector: %s' % reflector)
    # Open gRPC channels
    with utils.get_grpc_session(sender, GRPC_PORT) as sender_channel, \
            utils.get_grpc_session(reflector, GRPC_PORT) as reflector_channel:
        # Start the experiment
        srv6_pm.start_experiment(
            sender=sender_channel,
            reflector=reflector_channel,
            send_refl_dest='fd00:0:83::2',
            refl_send_dest='fd00:0:13::2',
            send_refl_sidlist=['fcff:3::1', 'fcff:4::1', 'fcff:8::100'],
            refl_send_sidlist=['fcff:4::1', 'fcff:3::1', 'fcff:1::100'],
            send_refl_localseg='fcff:8::100',
            refl_send_localseg='fcff:1::100',
            send_in_interfaces=[],
            refl_in_interfaces=[],
            send_out_interfaces=[],
            refl_out_interfaces=[],
            measurement_protocol='TWAMP',
            send_dst_udp_port=45678,
            refl_dst_udp_port=45678,
            measurement_type='LOSS',
            authentication_mode='HMAC_SHA_256',
            authentication_key='s75pbhd-xsh;290f',
            timestamp_format='PTPv2',
            delay_measurement_mode='OneWay',
            padding_mbz=10,
            loss_measurement_mode='Inferred',
            interval_duration=10,
            delay_margin=5,  # sec assert(<interval)
            number_of_color=2,  # sec assert(==2)
            force=True
        )


def start_experiment_no_measure_id():
    """Start a new experiment (without the measure_id)"""

    logger.info('*** Starting a new experiment')
    # IP addresses
    sender = 'fcfd:0:0:1::1'
    reflector = 'fcfd:0:0:8::1'
    logger.info('Sender: %s' % sender)
    logger.info('Reflector: %s' % reflector)
    # Open gRPC channels
    with utils.get_grpc_session(sender, GRPC_PORT) as sender_channel, \
            utils.get_grpc_session(reflector, GRPC_PORT) as reflector_channel:
        # Start the experiment
        srv6_pm.start_experiment(
            measure_id=100,
            sender=sender_channel,
            reflector=reflector_channel,
            send_refl_dest='fd00:0:83::/64',
            refl_send_dest='fd00:0:13::/64',
            send_refl_sidlist=['fcff:3::1', 'fcff:8::100'],
            refl_send_sidlist=['fcff:3::1', 'fcff:1::100'],
            send_refl_localseg='fcff:8::100',
            refl_send_localseg='fcff:1::100',
            send_in_interfaces=[],
            refl_in_interfaces=[],
            send_out_interfaces=[],
            refl_out_interfaces=[],
            measurement_protocol='TWAMP',
            send_dst_udp_port=45678,
            refl_dst_udp_port=45678,
            measurement_type='LOSS',
            authentication_mode='HMAC_SHA_256',
            authentication_key='s75pbhd-xsh;290f',
            timestamp_format='PTPv2',
            delay_measurement_mode='OneWay',
            padding_mbz=10,
            loss_measurement_mode='Inferred',
            interval_duration=10,
            delay_margin=10,
            number_of_color=3
        )


def get_experiment_results():
    """Get the results of a running experiment"""

    logger.info('*** Get experiment results')
    # IP addresses
    sender = 'fcfd:0:0:1::1'
    reflector = 'fcfd:0:0:8::1'
    logger.info('Sender: %s' % sender)
    logger.info('Reflector: %s' % reflector)
    # Open gRPC channels
    with utils.get_grpc_session(sender, GRPC_PORT) as sender_channel, \
            utils.get_grpc_session(reflector, GRPC_PORT) as reflector_channel:
        # Get the results
        results = srv6_pm.get_experiment_results(
            sender=sender_channel,
            reflector=reflector_channel,
            send_refl_sidlist=['fcff:3::1', 'fcff:4::1', 'fcff:8::100'],
            refl_send_sidlist=['fcff:4::1', 'fcff:3::1', 'fcff:1::100'],
        )
    # Check for errors
    if results is None:
        print('Error in get_experiment_results()')
        print()
        return
    # Print the results
    for result in results:
        print("------------------------------")
        print("Measurement ID: %s" % result['measure_id'])
        print("Interval: %s" % result['interval'])
        print("Timestamp: %s" % result['timestamp'])
        print("FW Color: %s" % result['fw_color'])
        print("RV Color: %s" % result['rv_color'])
        print("sender_seq_num: %s" % result['sender_seq_num'])
        print("reflector_seq_num: %s" % result['reflector_seq_num'])
        print("Sender TX counter: %s" % result['sender_tx_counter'])
        print("Sender RX counter: %s" % result['sender_rx_counter'])
        print("Reflector TX counter: %s" % result['reflector_tx_counter'])
        print("Reflector RX counter: %s" % result['reflector_rx_counter'])
        print("------------------------------")
        print()
    print()


def stop_experiment():
    """Stop a running experiment"""

    logger.info('*** Stopping experiment')
    # IP addresses
    sender = 'fcfd:0:0:1::1'
    reflector = 'fcfd:0:0:8::1'
    logger.info('Sender: %s' % sender)
    logger.info('Reflector: %s' % reflector)
    # Open gRPC channels
    with utils.get_grpc_session(sender, GRPC_PORT) as sender_channel, \
            utils.get_grpc_session(reflector, GRPC_PORT) as reflector_channel:
        # Stop the experiment
        srv6_pm.stop_experiment(
            sender=sender_channel,
            reflector=reflector_channel,
            send_refl_dest='fd00:0:83::2',
            refl_send_dest='fd00:0:13::2',
            send_refl_sidlist=['fcff:3::1', 'fcff:4::1', 'fcff:8::100'],
            refl_send_sidlist=['fcff:4::1', 'fcff:3::1', 'fcff:1::100'],
            send_refl_localseg='fcff:8::100',
            refl_send_localseg='fcff:1::100',
        )


# Entry point for this script
if __name__ == "__main__":
    # Enable debug mode
    debug = True
    # IP address of the gRPC server
    grpc_server_ip = '::'
    # Port of the gRPC server
    grpc_server_port = 50052
    # Port of the gRPC client
    grpc_client_port = 50052
    # Create a new SRv6 Controller
    Thread(
        target=srv6_pm.__start_grpc_server,
        kwargs={
            'grpc_ip': grpc_server_ip,
            'grpc_port': grpc_server_port,
            'secure': False
        }
    ).start()
    # Start a new experiment
    print()
    print()
    # start_experiment_no_measure_id()
    start_experiment()
    # Collects results
    for i in range(100):
        # Wait for 10 seconds
        time.sleep(10)
        # Get the results
        get_experiment_results()
    # Wait for few seconds
    time.sleep(2)
    # Stop the experiment
    stop_experiment()
    print()
    print()
