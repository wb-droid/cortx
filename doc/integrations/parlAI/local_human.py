#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""
Agent does gets the local keyboard input in the act() function.

Example: parlai eval_model -m local_human -t babi:Task1k:1 -dt valid
"""

from parlai.core.agents import Agent
from parlai.core.message import Message
from parlai.utils.misc import display_messages, load_cands
from parlai.utils.strings import colorize
import requests
import json

from waiting import wait
import os


class LocalHumanAgent(Agent):
    def add_cmdline_args(argparser):
        """
        Add command-line arguments specifically for this agent.
        """

        agent = argparser.add_argument_group('Local Human Arguments')
       
        


        agent.add_argument(
            '-fixedCands',
            '--local-human-candidates-file',
            default=None,
            type=str,
            help='File of label_candidates to send to other agent',
        )
        agent.add_argument(
            '--single_turn',
            type='bool',
            default=False,
            help='If on, assumes single turn episodes.',
        )

    def __init__(self, opt, shared=None):
        super().__init__(opt)
        self.id = 'localHuman'
        self.episodeDone = False
        self.finished = False
        self.fixedCands_txt = load_cands(self.opt.get('local_human_candidates_file'))
        print(
            colorize(
                "Enter [DONE] if you want to end the episode, [EXIT] to quit.",
                'highlight',
            )
        )

    def epoch_done(self):
        return self.finished

    def observe(self, msg):
        print(
            display_messages(
                [msg],
                
                prettify=self.opt.get('display_prettify', False),
            )
        )
 

    def act(self):
        reply = Message()
        print("reply:",reply)
        reply['id'] = self.getID()
   
        def is_something_ready(file):
            file = os.path.isfile(file)

            if file is True:
                return True
            return False




        # wait for something to be ready
        something = "input.txt"

        wait(lambda: is_something_ready(something), waiting_for="input.txt file to be ready")
        file = open("input.txt","r").read()
       
        text  = file.split("_")
        text = text[0]
        reply_text = text
        print("reply_text_initial",reply_text)
        reply['episode_done'] = False
        
        reply['label_candidates'] = self.fixedCands_txt
       
        reply['text'] = reply_text
        


   



        

       
        #reply = {'id': 'localHuman', 'episode_done': False, 'label_candidates': None, 'text': reply}
        #os.remove("input.txt")
        
        return reply


    def episode_done(self):
        return self.episodeDone