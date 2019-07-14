Unofficial Wearheart API
=====

## Introduction
My obsession with ECG haven't worn off yet, from the last project I use AD8232 module with Arduino but the issue is I've got to attach all the wires and electrodes to my body. To avoid the inconveniece, I search around for ECG wearable alternative, the iwatch I own is pretty much useless right now for ECG and they even disabled HRV for watch bought from the local store. Luckily I found relatively inexpensive smart watch that supports not only ECG but blood pressure.

I found the concept is interesting, we can actually use PPG and ECG to measure the blood pressure, to explain it simply: PPG waveform is produced from the blood concentration in arteries while ECG is produced from the heart electrical signal. There is actually a delay between the peak signal in ECG and the PPG wave. Scientifically they call this delay as PWTT or pulse wave transit time. Intuitively the higher the blood pressure the faster the blood travels in artery and resulting the shorter delay between the ECG peak signal and PPG wave. If you're interested to get more details you may read [here](https://eu.nihonkohden.com/en/innovativetechnologies/pwtt/howitworks.html)


## N58 Watch

<img width=300 src="images/IMG_2572.JPG?raw=true"/>

## Shareable ECG wave from Wearheart App

<img width=300 src="images/6.png?raw=true"/>

## Reverse Engineering
Before I proceeded to this not so "ethically" stuff, I really did googled for any API or SDK provided to get the data. The Wearheart app didn't even update ihealth and no official API. The only one choice left, we must do "surgery". 

### Man in the middle attack (MITM)
Often time, MITM is enough to extract internal communication between the app and the cloud, I use Charles proxy and the result, walla:

<img width=500 src="images/5.png?raw=true"/>

The app communicate to **wearheart.cn** but do you noticed that? It was sending my sensitive health data by using non https? 

Okay well, looks like the requests and responses are **base64** encoded.

### Decode the response
I use online service to decode the content.

<img width=500 src="images/4.png?raw=true"/>

What in the world are these characters? I know the app is developed from China, but I don't suppose they communicate using Chinese character. I did't read Chinese so I google translate the decoded content. Still looks like unintelligible.

### Decompile The App
I believed it was somehow encrypted. Who on earth would transmit sensitive clear text using unencrypted channel right? My first guess was the app probably carry private/public keys to encode and decode the message. Extracting the apk is as easy as unzip any of zipped file.

After minutes looking around for any cert files, I gave up. Just look into the codes already. So I decompiled the apk and the search for clues begun.

The codes is as expectedly obfuscated, but we already knew from above steps that there has to be part that dealt with **JSON**. After patiently search for JSON from "find in path" in Android Studio, I found an interesting procedure that is used multiple times.

<img width=500 src="images/1.png?raw=true"/>

It looks like the function try to transform the JSON object into something else. Let's dig deeper.

<img width=500 src="images/2.png?raw=true"/>

Well, at this point I was pretty sure the line 32 is encryption key. So It's just a symmetric encryption. The **m11794a** function should reveals us the clue about what type of encryption used.

<img width=500 src="images/3.png?raw=true"/>

Yeah, pretty straight forward. It's AES.

## How do I use the SDK or the API?

Please view the example in [Example of API usage.ipynb](Example of API usage.ipynb)


## TODO

Given the limitation of wearheart itself such as no raw hrv computed and the result isn't written to ihealth, plus the data safety issues, I'm planning to create another app that can read and send command directly to the watch via bluetooth. I bought HM-10 to perform MITM on the bluetooth level. So stay tuned.


<img width=300 src="images/IMG_2573.JPG?raw=true"/>
