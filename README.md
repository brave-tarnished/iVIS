A proof-of-concept license plate recognition system using:
* OpenMV 7 to capture images and pre-process them.
* Local LLM (LLaVa-phiu-3-mini) for performing OCR and text-extraction.
* STM32F4 to control a miniature vehicle barrier using a servo motor in the demo setup – allowingauthorized vehicles to pass, raising alarms for unauthorized ones, and displaying license plate details on an LCD screen.
* ESP32 to transmit plate data and metadata to a web application.
