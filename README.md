# IMoH
Crawling [Israel's Ministry of Health's epidemiological weekly reports](http://www.health.gov.il/UnitsOffice/HD/PH/epidemiology/Pages/epidemiology_report.aspx)

This is the helper package for [Epidemic](http://epidemic.co.il) that deals with crawling

Installing this package installs the command line utility `imoh`

## Commands
* `imoh arrange` Arrange data into machine readable format
* `imoh download` Download all reports
* `imoh purge` Delete all files in data folder
* `imoh refresh` Refresh reports (Force Download)
* `imoh create` purge, refresh, arrange
