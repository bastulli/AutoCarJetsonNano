# AutoCarJetsonNano
PyTorch Python Neural Network Autonomous 1/10 Car for Nvidia Jetson Nano

![Jetson Nano 1/10th RC Car](media/carbg.png)

![Demo](https://media.giphy.com/media/jn2q3m1mUHt7hx2DQe/giphy.gif)

## BOM

* **System Hardware**
    * Servo Driver https://www.amazon.com/dp/B014KTSMLA/ref=cm_sw_r_tw_dp_U_x_.PW4CbAD5YKP4
    * Jetson Nano https://store.nvidia.com/store?Action=DisplayPage&Locale=en_US&SiteID=nvidia&id=QuickBuyCartPage
    * Camera https://leopardimaging.com/product/li-imx219-mipi-ff-nano/
    * Wifi Chip https://www.amazon.com/gp/product/B01MZA1AB2/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1
    * Wifi Attenna https://www.arrow.com/en/products/2042811100/molex
    * PS4 Controller https://www.amazon.com/dp/B01LWVX2RG/ref=cm_sw_r_tw_dp_U_x_USW4CbEXZK23G

* **Car**
    * 1/10 4wd Car chassis https://www.amazon.com/dp/B00NYR8D1O/ref=cm_sw_r_tw_dp_U_x_zIW4Cb721TVKE
    * Brushed Motor https://hobbyking.com/en_us/540-6527-brushed-motor-90w.html
    * Standard Analog Servo https://hobbyking.com/en_us/hobbykingtm-hk15138-standard-analog-servo-4-3kg-0-17sec-38g.html
    * 45A Brushed Car ESC https://hobbyking.com/en_us/hobbyking-x-car-45a-brushed-car-esc.html
    * 5000mAh 2S 7.4V 60C https://hobbyking.com/en_us/turnigy-5000mah-2s-7-4v-60c-hardcase-pack-roar-approved.html

* **Accessories**
    * Nylon Standoffs https://www.amazon.com/dp/B015S27EG2/ref=cm_sw_r_tw_dp_U_x_LXW4Cb35VNVK2
    * SD card https://www.amazon.com/dp/B06XX29S9Q/ref=cm_sw_r_tw_dp_U_x_cYW4Cb3YZFVXY
    * Wires https://www.amazon.com/dp/B01BV3Z342/ref=cm_sw_r_tw_dp_U_x_7YW4CbB36CAF7

## How to use

Install python requirements. Install ds4drv and connect PS4 Bluetooth controller to Ubuntu. Inside AutoCarJetsonNano/car, start main.py and drive car around.  Images are captured when speed is > 0.  After driving car around, offload images to remote computer for training and copy control_data.csv .  Start autocar via Jupyter Lab or Notebook and train model via pytorch. Load model back to Nano after training and start main.py  Press X to launch autopilot.