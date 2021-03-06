/*
* Licensed to the Apache Software Foundation (ASF) under one
* or more contributor license agreements.  See the NOTICE file
* distributed with this work for additional information
* regarding copyright ownership.  The ASF licenses this file
* to you under the Apache License, Version 2.0 (the
* "License"); you may not use this file except in compliance
* with the License.  You may obtain a copy of the License at
*
*   http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing,
* software distributed under the License is distributed on an
* "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
* KIND, either express or implied.  See the License for the
* specific language governing permissions and limitations
* under the License.
*/

module.exports.blacklist = [
    '-cases.html',
    'geo-random-stream.html',
    'chord.html',
    'lines-ny.html',
    'lines-ny-appendData.html',
    'linesGL-ny-appendData.html',
    'richText.html',
    'tmp-base.html',

    'finished-gl.html',
    'scatter-gps.html',
    'webkit-dep.html',

    // Mobile
    'mobileBench.html',
    'touch-test.html',

    // Image size not match
    'symbol2.html',

    // This case will have timeout
    'visualMap-performance1.html',
    'lines-bus.html',
    'lines-stream-not-large.html'
];


module.exports.SVGBlacklist = [
    'bar-stream-large.html',
    'bar-stream-large1.html',
    'candlestick-large2.html'
];