Unofficial Wearheart API
=====

## Introduction
My obsession with ECG haven't worn off yet, from the last project I use AD8232 module with Arduino but the issue is I've got to attach all the wires and electrodes to my body. To avoid the inconveniece, I search around for ECG wearable alternative, the iwatch I own is pretty much useless right now for ECG and they even disabled HRV for watch bought from the local store. Luckily I found relatively inexpensive smart watch that supports not only ECG but blood pressure.

I found the concept is interesting, we can actually use PPG and ECG to measure the blood pressure, to explain it simply: PPG waveform is produced from the blood concentration in arteries while ECG is produced from the heart electrical signal. There is actually a delay between the peak signal in ECG and the PPG wave. Scientifically they call this delay as PWTT or pulse wave transit time. Intuitively the higher the blood pressure the faster the blood travels in artery and resulting the shorter delay between the ECG peak signal and PPG wave. If you're interested to get more details you may read [here](https://eu.nihonkohden.com/en/innovativetechnologies/pwtt/howitworks.html)


## N58 Watch

<img width=300 src="images/IMG_2572.JPG?raw=true"/>

## Shareable ECG wave from Wearheart App
<img width=300 src="images/6.png?raw=true"/>
