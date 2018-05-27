# the-arrrbitrage
The Arrrbitrage is a basic platform for pillaging data from cryptocurrency exchanges with a focus on the Australian investor. The display url is: https://contrarian.netlify.com/ with the corresponding [website git repository](https://github.com/Tehsurfer/hugo-contrarian)
## Set up ye ship 
The project was not originally made with the intention of distribution. But if you are interested in running it here are some recommended steps:
1. Download repository to a folder 
1. Open Command prompt and run `python setup.py install` 
1. Download [Dropbox for desktop](https://www.dropbox.com/install) 
1. Change the path in settings.py to a path in your Dropbox folder 
1. Disable the git-update part of the software (unless you want to downlaod hugo and create a website)
1. Disable the exchange rates, use a free one such as: https://openexchangerates.org/
1. Disable text alerts or create a twilio account (not free)
### When the seas get rough 
There is a chance that all external libraries might not load via the settings.py file. In this case I would use `pip install package` where package is the unloaded python library 
## Thanks to the following open source projects
1. [ccxt](https://github.com/ccxt/ccxt#ccxt--cryptocurrency-exchange-trading-library) 
1. [Netlify](https://www.netlify.com/) 
1. [Hugo](https://github.com/gohugoio/hugo)
