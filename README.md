Realizați un utilitar care să managerieze o listă de parole sub forma unui fișier, care poate fi
actualizat (insert / update / delete), înăuntrul căruia parolele sunt criptate (cu o parolă master
ce va trebui introdusă la deschiderea fișierului).

INPUT:
  pwmanager.py <master_password> -<operation> <website> <username> <password>
  pwmanager.py <master_password> -add gmail.com johndoe@google.com cookie123
  pwmanager.py <master_password> -get gmail.com
  pwmanager.py <master_password> -remove gmail.com
  pwmanager.py <master_password> -list
  
OUTPUT: pwmanager.db
