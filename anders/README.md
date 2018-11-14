## database integration

  - establish database structure
  
  - requirements: postgresql, python 3
  - dependencies: psycopg2, psycopg2.extras, psycopg2.extensions

    - establish I/O for each component (in development)
  		- initial content to load into db:
  			- mri
  			- ct
  			- signal files
  			- eeg channel coordinates (hard coded)
		- pull from db:
  			- mri
  			- ct
  			- smr
  			- signal files
  			- channel coordinates
  			- channel scores
  		- push to db:
  			- stripped skull (smr)
  			- eeg coordinates
  			- ecog coordinates
  			- channel scores