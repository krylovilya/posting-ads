1) [Основы Web-безопасности](#Основы-Web-безопасности)
2) [Политики безопасности и протоколы](#Политики-безопасности-и-протоколы)
   1) [CSP (Политика защиты контента)](#csp-политика-защиты-контента)
   2) [TLS (Безопасность Транспортного Уровня)](#tls-безопасность-транспортного-уровня)
3) [Три главных цели безопасности](#три-главных-цели-безопасности)
4) [Виды угроз](#виды-угроз)
   1) [XSS (Межсайтовый скриптинг)](#xss-межсайтовый-скриптинг)
   2) [CSRF (Подделка межсайтовых запросов)](#csrf-подделка-межсайтовых-запросов)
   3) [SQL injection (SQL-инъекции)](#sql-injection-sql-инъекции)
   4) [Clickjacking (англ. «захват клика»)](#clickjacking-англ-захват-клика)
5) [Методы защиты](#методы-защиты)
   1) [Проверка сайта на уязвимости](#проверка-сайта-на-уязвимости)
   2) [Использование защищенных протоколов передачи данных](#использование-защищенных-протоколов-передачи-данных)
   3) [Применение ПО, обеспечивающего безопасность](#применение-по-обеспечивающего-безопасность)
   4) [Дополнительные способы обеспечения безопасности](#дополнительные-способы-обеспечения-безопасности)
6) [Защита от угроз в Django](#защита-от-угроз-в-django)
   1) [Защита от XSS](#защита-от-xss)
   2) [Защита от CSRF](#защита-от-csrf)
   3) [Защита от SQL инъекции](#защита-от-sql-инъекции)
   4) [Защита от clickjacking](#защита-от-clickjacking)
   5) [SSL/HTTPS](#sslhttps)
   6) [Валидация заголовка Host](#валидация-заголовка-host)

### Основы Web безопасности

- Никогда не доверяйте данным из браузера.
- Используйте более эффективное управление паролями:
  - поощряйте регулярную смену надёжных паролей,
  - рассмотрите возможность двухфакторной аутентификации.
- Настройте свой веб-сервер для использования HTTPS/HSTS.
- Следите за наиболее популярными угрозами и в первую очередь устраняйте наиболее распространённые уязвимости.
- Используйте инструменты сканирования уязвимостей, чтобы выполнить автоматическое тестирование безопасности на вашем сайте.
- Храните и отображайте только те данные, которые вам нужны.

### Политики безопасности и протоколы

#### CSP (Политика защиты контента)

это дополнительный уровень безопасности, позволяющий распознавать и устранять определённые
типы атак, таких как Cross Site Scripting (XSS) и атаки внедрения данных. 
Спектр применения этих атак включает, но не ограничивается кражей данных,
подменой страниц и распространением зловредного ПО.

Настройка CSP включает в себя добавление на страницу HTTP-заголовка
Content-Security-Policy и его настройку в соответствии со списком
доверенных источников, из которых пользователь может получать контент. 
Например, страница, на которой происходит загрузка и отображение изображений 
может разрешать их получение из любых источников, но ограничить отправку данных 
формы конкретным адресом. При правильной настройке, Content Security Policy 
поможет защитить страницу от атак межсайтового скриптинга.

#### TLS (Безопасность Транспортного Уровня)

это протокол для организации защищённой передачи данных через интернет,
предотвращая взлом и прослушивание электронной почты, просмотра сайтов,
переписки и прочих протоколов.

HTTP, зашифрованный с использованием TLS, обычно называется HTTPS. 
Зашифрованный TLS веб-трафик по соглашению обменивается по порту 443 
по умолчанию, тогда как незашифрованный HTTP использует по умолчанию 
порт 80. HTTPS остается важным вариантом использования TLS. 

### Три главных цели безопасности:

1) конфиденциальность - доступность информации только авторизованным пользователям, процессам и устройствам,
2) целостность - ценная информация должна храниться/обрабатываться/передаваться без искажений, с использованием хеширования,
3) доступность - обеспечение своевременного и надежного доступа к информации и информационным сервисам.

### Виды угроз:

#### XSS (Межсайтовый скриптинг) 
это термин, используемый для описания типа атак, 
которые позволяют злоумышленнику внедрять вредоносный код через веб-сайт в
браузеры других пользователей. Поскольку внедрённый код поступает в браузер
с сайта, он является доверенным и может выполнять такие действия,
как отправка авторизационного файла cookieпользователя злоумышленнику. 
Когда у злоумышленника есть файл cookie, он может войти на сайт,
как если бы он был пользователем, и сделать все, что может пользователь,
например, получить доступ к данным кредитной карты, просмотреть
контактные данные или изменить пароли.

Наилучшей защитой от уязвимостей XSS является удаление или отключение
любой разметки, которая потенциально может содержать инструкции по запуску кода.
Для HTML это включает такие элементы, как ```<script>, <object>, <embed> и <link>```.

#### CSRF (Подделка межсайтовых запросов)

SRF-атаки позволяют злоумышленнику выполнять действия,
используя учётные данные другого пользователя, без его ведома или согласия.

Один из способов предотвратить этот тип атаки - запросить сервером запросы POST,
содержащие секрет, созданный пользователем для конкретного сайта.
Веб-фреймворки часто включают такие механизмы предотвращения CSRF.

#### SQL injection (SQL-инъекции)

Уязвимости SQL-инъекций позволяют злоумышленникам выполнять произвольный код 
SQL в базе данных, позволяя получать, изменять или удалять данные независимо
от разрешений пользователя. Успешная инъекционная атака может подделать 
удостоверения, создать новые удостоверения с правами администратора, 
получить доступ ко всем данным на сервере или уничтожить / изменить данные,
чтобы сделать их непригодными для использования.

Чтобы избежать такого рода атак, вы должны убедиться, что любые пользовательские
данные, которые передаются в запрос SQL, не могут изменить природу запроса.
Один из способов сделать это - экранировать все символы пользовательского ввода, 
которые имеют особое значение в SQL.

Веб-фреймворки будут часто заботиться о зарезервированных символах для вас.
Django, например, гарантирует, что любые пользовательские данные, передаваемые
в наборы запросов (модельные запросы), экранируются.

#### Clickjacking (англ. «захват клика»)

Атака типа clickjacking (англ. «захват клика») позволяет вредоносной 
странице кликнуть по сайту-жертве от имени посетителя.

Многие сайты были взломаны подобным способом, включая 
Twitter, Facebook, Paypal и другие. Все они, конечно же, сейчас защищены.

В качестве защиты ваш сайт может предотвратить встраивание себя 
в iframe на другом сайте, установив соответствующие заголовки HTTP.

### Методы защиты

#### Проверка сайта на уязвимости

Прежде чем разрабатывать методику защиты веб-приложения от потенциальных угроз,
сайт следует проверить на уязвимости. Проверка проводится ручным или
автоматизированным способом. Программы, доступные в платной и бесплатной версиях,
протестируют приложение на основные риски. Такие программные продукты существуют
в двух вариантах: Black hat, моделирующие действия взломщиков, и White hat,
планомерно выявляющие все недочеты системы методом сканирования.

Используя платные или бесплатные ресурсы мониторинга систем безопасности 
необходимо проверить гипотетическую возможность хакера обойти требования 
обязательной аутентификации, предусмотренные для некоторых страниц веб-приложения.
Для этого нужно использовать такие традиционные способы взлома как смена параметров
URL (в частности, ID пользователя) или смена Cookie. 

#### Использование защищенных протоколов передачи данных

HTTPS (Hyper Text Transfer Protocol Secure) защищает информацию о пользователе 
веб-приложения при помощи шифрования трафика. Он обеспечивает сохранение 
конфиденциальности и целостности информации, не допуская утечку или подмену данных. 

Большинство ресурсов использует технологию давно, это стало хорошим тоном,
подтверждающим готовность их владельцев защищать интересы клиентов.
Поисковик Google поднимает в выдаче сайты, использующие эту технологию.

HTTPS необходим, если пользователи передают сервису такие сведения, как:
* номера кредитных карт;
* персональные данные;
* адреса страниц, на которые они заходят.

Дополнительной возможностью после настройки HTTPS станет применение
Hyper Strict Transport Security (HSTS). 
Это опция принудительного использования протокола HTTPS, 
даже если сервер не поддерживает его применение. Однако и защищенные протоколы
не спасут веб-приложение, если само программное обеспечение устарело. 

#### Применение ПО, обеспечивающего безопасность

Владелец приложения должен держать руку на пульсе обновлений программного
обеспечения. Хакеры тестируют все обновления и находят в них уязвимости
иногда раньше, чем разработчики. Особенно активно взламываются операционные
системы, технологии управления HTTP и системы управления контентом (CMS).

Web-сайты часто имеют зависимые компоненты (программные модули менеджмента 
контента). Для управления ими используются менеджеры пакетов, например,
Composer, NPM или RubyGems. За их обновлениями во избежание проблем 
безопасности также необходимо следить. 

#### Дополнительные способы обеспечения безопасности 

Работа с веб-сервисами требует использования широкого инструментария для обеспечения
безопасности. Помимо основных перечисленных методов, часто применяются:

* шифрование паролей;
* избегание межсайтового скриптинга;
* контроль загрузки файлов на сервер.

Совместное применение всех доступных решений обеспечит безопасность
на максимально доступном уровне.  

### Защита от угроз в Django

Хорошей новостью для всех разработчиков, использующих Django, является то, что большинство известных атак обрабатывается
фреймворком!

#### Защита от XSS

Система шаблонов Django защищает от большинства XSS-атак, экранируя определённые символы, считающиеся "опасными" в HTML.

Использование шаблонов Django защищает вас от большинства XSS-атак. Однако существует возможность отключения данной
защиты, при котором экранирование не будет автоматически применятся ко всем полям, которые не должны будут заполнятся
пользователем(к примеру, поле `help_text` обычно заполняется не пользователем, поэтому Django не будет экранировать его
значение).

Так же XSS-атаки могут быть осуществлены через другие ненадёжные источники данных, такие как cookies, сторонние сервисы
или загруженные файлы (и прочие источники, данные которых не были специально обработаны перед отображением на странице).
Если вы отображаете данные из этих источников, вы должны добавить ваш собственный обработчик для фильтрации данных.

#### Защита от CSRF

Django генерирует уникальный для пользователя/браузера токен и отклоняет все формы, которые не содержат его или содержат
его неверное значение.

Для использования данного вида атак, хакер должен найти и добавить верный CSRF токен для каждого выбранного целью
пользователя. Это означает, что хакер теперь не может использовать массовые рассылки с вредоносными файлами, так как для
каждого из них CSRF токен будет уникальным.

Защита Django от CSRF атак по умолчанию включена. Вам всегда следует использовать тег `{% csrf_token %}` в ваших формах
и использовать POST для запросов, которые могут изменить или добавить данные в вашу базу данных.

#### Защита от SQL инъекции

Уязвимость SQL инъекции позволяет атакующему выполнить произвольный SQL код в базе данных и получить доступ к данным (
прочитать, отредактировать и изменить) независимо от текущих прав доступа пользователя. В большинстве случаев вы будете
получать доступ к данным базы данных, используя сущности `queryset/model` Django. Используя их для генерации SQL
запросов, вы получите корректно сформированный и экранированный запрос для выбранной базы данных. Если вам необходимо
писать "сырые" запросы, вам так же нужно будет продумать защиту от инъекций.

#### Защита от clickjacking

В данном виде атак атакующий перехватывает ввод на видимом слое страницы и перенаправляет их на скрытый слой под ним.
Этот метод может быть использован к примеру для отображения официального сайта банка, с перехватом данных для входа в
невидимом `<iframe>`, который контролирует атакующий. Django содержит защиту от кликджекинга в виде промежуточного
програмного обеспечения (middleware) X-Frame-Options, который поддерживается браузерами и может запретить отображение
страницы внутри `<iframe>`.

#### SSL/HTTPS

SSL/HTTPS может быть использован на веб-сервере для шифрования всего трафика между сервером и пользователем, включая
данные входа, которые иначе будут отправляться как обычный текст (который сможет прочитать любой перехвативший запрос
человек). Использование HTTPS высоко рекомендовано. Если используется HTTPS, Django позволяет использовать следующие
методы защиты:

* _SECURE_PROXY_SSL_HEADER_ может быть использовано для проверки, что всегда используется безопасное подключение, даже
  если данные поступают из прокси, использующего протокол отличный от HTTP.
* _SECURE_SSL_REDIRECT_ используется для перенаправления всех запросов с HTTP на HTTPS.
* _Используйте HTTP Strict Transport Security (HSTS)_. Этот HTTP заголовок информирует браузер о том, что все
  последующие запросы должны всегда использовать HTTPS. Совместно с перенаправлением HTTP запросов на HTTPS, эта опция
  позволяет обеспечить использование HTTPS в каждом запросе. HSTS может так же быть настроен опциями _
  SECURE_HSTS_SECONDS_ и
  _SECURE_HSTS_INCLUDE_SUBDOMAINS_ или на веб-сервере.
* Используйте ‘безопасные’ cookies выставив _SESSION_COOKIE_SECURE_ и _CSRF_COOKIE_SECURE_ в _True_. Это позволит
  обеспечить пересылку данных cookies только через протокол HTTPS.

#### Валидация заголовка Host

Используйте _ALLOWED_HOSTS_, чтобы принимать только запросы от доверенных хостов.
