#  Bot in the Shell #
## Разворачиваем среду разработки ##
Клонируем проект, переходим в папку проекта и выполняем:
> sudo bash start.sh

Должно развернуться окружение со всеми необходимыми пакетами. В дальнейшем при обновлении файлов Pipfile и Pipfile.lock в репозитории необходимо выполнить команду

> pipenv shell | pipenv install

Будут установлены пакеты из Pipfile.lock. Далее необходимо создать (скопировать из примера) файл .env в корне проекта и сконфигурировать переменные окружения (этот файл используется по умолчанию при активации окружения).

Для использования интерпретатора Pipenv в PyCharm нужно выполнить команду, после чего в настройках IDE установить виртуальное окружение. После этого станут доступны для просмотра кода внешние библиотеки.
> pipenv --venv

В директории configs расположены различные заготовки конфигурационных файлов (например, для тестирования определенной стратегии, пары и т.д.). Чтобы подключить окружение с этим конфигом нужно выполнить команду:
> PIPENV_DOTENV_LOCATION=configs/.env.test pipenv shell

## Команды ##

Список предустановленных команд:
> pipenv scripts

Чтобы запустить команду:
> pipenv run scriptName

Другая информация по конфигурации окружения [здесь](https://pipenv.pypa.io/en/latest/advanced/#automatic-loading-of-env).

## Документация ##

При написании новых классов, функций и т.д. нужно описывать, что они делают при помощи многострочных комментариев

Возможно автоматически сгенерировать описание по списку скриптов (указываются от директории src в файле listForDocumentation.txt) при помощи команды:
> pipenv run generateDocumentation

Пока что примитивно. При необходимости доработаем.