// Copyright 2016, Google, Inc.
// Licensed under the Apache License, Version 2.0 (the 'License');
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//    http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an 'AS IS' BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

'use strict';

process.env.DEBUG = 'actions-on-google:*';
const {DialogflowApp} = require('actions-on-google');
const functions = require('firebase-functions');
const _ = require('underscore');

exports.nia = functions.https.onRequest((request, response) => {
  const app = new DialogflowApp({request, response});
  let networkFunctions = '';
  let policyTarget = '';
  let networkIntentProgram = '';

  function policyTargetIntent (app) {
    networkFunctions = app.getArgument('network-function');
    app.ask(
      'Okay, so you want to use ' +
        _.map(networkFunctions, (nf, index) => {
          return index === networkFunctions.length - 1
            ? ', and a'
            : 'a ' + nf + (index === networkFunctions.length - 1) ? ', ' : '.';
        }) +
        ' For whom do you want to use these functions?',
      ['I`m sorry. I didn`t get that. Who do you want to use the functions?']
    );
  }

  function networkProgramIntent (app) {
    networkFunctions = app.getArgument('network-function');
    policyTarget = app.getArgument('policy-target');
    console.log('args', networkFunctions, policyTarget);
    networkIntentProgram =
      'define intent userIntent:' +
      '\n   add ' +
      _.map(networkFunctions, nf => nf + ', ') +
      '\n   for ' +
      _.map(policyTarget, pt => pt + ', ');

    app.ask('The info you gave me generated this program:\n ' + networkIntentProgram + '\n Is this what you want?', [
      'Sorry, can you repeat?',
      'Is this what you want?'
    ]);
  }

  const actionMap = new Map();
  actionMap.set('input.target', policyTargetIntent);
  actionMap.set('input.program', networkProgramIntent);

  app.handleRequest(actionMap);
});
