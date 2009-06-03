"""Setup the swat application"""
import logging

from swat.config.environment import load_environment

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup swat here"""
    load_environment(conf.global_conf, conf.local_conf)
