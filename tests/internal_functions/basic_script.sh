#!/bin/bash
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


f(){
    echo ' terminate ';
    echo ' terminate ' >&2;
    for i in $(seq 1 $1); do sleep 1; done
    exit 10
}

trap "f $2" TERM
for i in {1..2}; do
    echo " stdout $i ";
    echo " stderr $i " >&2;
    for k in $(seq 1 $1); do sleep 1; done
done
exit 0
