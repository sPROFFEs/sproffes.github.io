---
categories:
- Recognition
- Sniffers
date: 2024-01-19
lang: en
original_lang: es
tags:
- sniffers
- wireshark
- tcpdump
- network-analysis
title: Sniffers
---

## Concepto

Within a computer interconnection called a network the equipment is hosts or nodes.

When we are within this network we can exchange data by cable or WiFi.

These data are bytes and must be interpreted for what network protocols are used, which is a set of rules that apply to network information to interpret it.

A sniffer monitors all network traffic both in and out within the network.

All these data that are exchanged with the different nodes or internet networks are called network packages.

There are times when we cannot use active recognition techniques or, for example, vulnerability detection or vulnerability analysis, because the systems that are connected to the network are so old and so sensitive that this additional traffic, that anomalous traffic that generate these active detection tools, can in some case cause the inavailability of any of the systems and that this affects the network infrastructure or the technological infrastructure in general.

So, in these cases, one of the options to try to direct our attacks a little more when it comes to exploiting a certain vulnerability can be to take a sniffer, put it into that infrastructure, simply copying that network traffic, that is, monitoring all the network activity and depending on the protocols it begins to intercept.

Depending, for example, on some values that have certain fields of the layers of the network packages, we can identify which applications are installed in the different nodes of that network and also what programs they use and what versions of those programs.

## Wireshark

It is a tool of the best known and powerful that by default in Kali is already installed.

! [https: / / www.wireshark.org / download] (/ assets / img / posts / recognition / 20241126 _ 000918 _ 89-1.png)

! [] (/ assets / img / posts / recognition / 20241126 _ 000924 _ 89-2.png)

The packages are divided into layers

! [] (/ assets / img / posts / recognition / 20241126 _ 000935 _ 89-3.png)

To view the packages in which the DNS names have been consulted we click on the magnifying glass

! [] (/ assets / img / posts / recognition / 20241126 _ 000953 _ 89-4.png)

! [] (/ assets / img / posts / recognition / 20241126 _ 001008 _ 89-5.png)

This is where the request is made to resolve that domain name

! [] (/ assets / img / posts / recognition / 20241126 _ 001103 _ 89-6.png)

Here we see the answers with the hosts and their IP both IPV4 and IPV6 as seen in the following package

! [] (/ assets / img / posts / recognition / 20241126 _ 001128 _ 89-7.png)

Well, you know HTTP goes above the TCP layer and many times when we are exchanging information that is very large, as can be for example a website, in the end we make a request to the web server, we tell him.

Hey, send me that website.

The web server sends you to the web page.

But of course, a website is a lot of information.

Okay, so the network packages or the amount of information that goes in a bit ristra that is exchanged, is limited in size. It's not an infinite size. And so, if the website or information we exchange is too big, we can't send it all in the same segment, in the same bit ristra or in the same network package.

So, we have to fragment that information somehow and send it in different segments or in different network packages.

## TCPDump

It differs from wireshark in that it uses a command console interface.

! [] (/ assets / img / posts / recognition / 20241126 _ 001708 _ 90-1.png)

These are just some of the options you offer, in your documentation you can find many more.

```bash
sudo tcpdump -D
```

! [Show network interfaces] (/ assets / img / posts / recognition / 20241126 _ 001734 _ 90-2.png)

```bash
sudo tcpdump -i eth0
```

! [Capture in network interface] (/ assets / img / posts / recognition / 20241126 _ 001804 _ 90-3.png)

Show more information:

```bash
sudo tcpdump -v -i eth0
sudo tcpdump icmp -i eth0
```

! [Filter protocols] (/ assets / img / posts / recognition / 20241126 _ 001924 _ 90-4.png)

```bash
sudo tcpdump host 185.230.63.107 -i eth0
```

! [Filter by host address] (/ assets / img / posts / recognition / 20241126 _ 001952 _ 90-5.png)

Save the capture to be later analyzed with Wireshark

```bash
sudo tcpdump -i eth0 -w Desktop/capture.pcap
```

Open the capture but with TCPDump and filter protocols

```bash
sudo nmap -n port 53 -v -r capture.pcap
sudo nmap -n port 80 -v -r capture.pcap | grep gamivo.com
```