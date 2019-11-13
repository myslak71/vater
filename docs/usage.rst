=====
Usage
=====

Scripts
'''''''

.. code-block:: Python

   >>> import vater
   >>> client = vater.Client(base_url='https://wl-api.mf.gov.pl')
   >>> client.search_nip(nip='1111111111')
   (
     Subject(
       name='Beastie Boys',
       nip='1111111111',
       status_vat='Czynny',
       regon='111111111',
       pesel=None,
       krs='1111111111',
       residence_address=None,
       working_address='Brooklyn',
       representatives=[],
       authorized_clerks=[],
       partners=[
         Company(
           company_name='Mike D',
           first_name='Michael',
           last_name='Diamond',
           nip=None,
           pesel=None
         )
       ],
       registration_legal_date=datetime.date(2001, 1, 1),
       registration_denial_basis=None,
       registration_denial_date=None,
       restoration_basis=None,
       restoration_date=None,
       removal_basis=None,
       removal_date=None,
       account_numbers=['11111111111111111111111111'],
       has_virtual_accounts=False
     ),
     'z5x71-85a8gl5'
   )

If you want to get raw server json just set ``raw`` to True:

.. code-block:: Python

   >>> client.search_nip(nip='1111111111', raw=True)
   {
     'result': {
       'subject': {
           'name': 'Eminem',
           'nip': '6969696969',
           'statusVat': 'Active',
           'regon': '777777777',
           'pesel': '77777777777',
           'krs': '6969696969',
           'residenceAddress': '8 mile',
           'workingAddress': '8 mile',
           'representatives': [
               {
                 'companyName': 'Moby Dick Inc',
                 'firstName': 'sir Richard',
                 'lastName': 'Lion Heart',
                 'nip': '6969696969',
                 'pesel': '77777777777'
               }
           ],
           'authorizedClerks': [],
           'partners': [],
           'registrationLegalDate': '2001-01-01',
           'registrationDenialBasis': 'Denial Basis',
           'registrationDenialDate': '2002-02-02',
           'restorationBasis': 'Restoration Basis',
           'restorationDate': '2003-03-03',
           'removalBasis': 'Removal Basis',
           'removalDate': '2004-04-04',
           'accountNumbers': ['11111111111111111111111111'],
           'hasVirtualAccounts': False
     },
     'requestId': 'aa111-aa111aaa',
     }
   }

By default the data is fetched from today's date,
it can be changed by setting ``date`` argument:

.. code-block:: Python

   >>> import datetime
   >>> client.search_nip(nip='1111111111', date=datetime.date(2001, 1, 1))

String may also be passed as a ``date``\ :

.. code-block:: Python

   >>> client.search_nip(nip='1111111111', date='2001-01-01')

Keep in mind the API limits maximum number of requested subjects to 30.

CLI
'''

.. list-table:: Commands
   :widths: 20
   :header-rows: 1

   * - command
   * - ``vater search-nip [ACCOUNT]``
   * - ``vater search-nip [ACCOUNTS]``
   * - ``vater search-nip [NIP]``
   * - ``vater search-nips [NIPS]``
   * - ``vater search-nips [REGON]``
   * - ``vater search-nips [REGONS]``
   * - ``vater check-nip [NIP] [ACCOUNT]``
   * - ``vater check-regon [REGON] [ACCOUNT]``

.. list-table:: Parameters
   :widths: 10 15 25
   :header-rows: 1

   * - parameter
     - default
     - description
   * - ``--date``
     - today
     - date in YYYY-MM-DD format
   * - ``--url``
     - https://wl-api.mf.gov.pl
     - vat register API url
