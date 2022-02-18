// Для относительных путей
const path = require('path');
// https://github.com/jantimon/html-webpack-plugin#options
const HTMLWebpackPlugin = require('html-webpack-plugin');
// https://github.com/johnagan/clean-webpack-plugin
const {CleanWebpackPlugin} = require('clean-webpack-plugin');
// https://www.npmjs.com/package/copy-webpack-plugin
const CopyWebpackPlugin = require('copy-webpack-plugin');
// https://webpack.js.org/plugins/mini-css-extract-plugin/
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
// https://www.npmjs.com/package/optimize-css-assets-webpack-plugin
const OptimizeCssAssetsPlugin = require('optimize-css-assets-webpack-plugin');
// https://webpack.js.org/plugins/terser-webpack-plugin/
const TerserPlugin = require('terser-webpack-plugin');
// https://www.npmjs.com/package/webpack-bundle-analyzer
const {BundleAnalyzerPlugin} = require('webpack-bundle-analyzer');

class Main {
    constructor(isDev,
                PathApp,
                PathOutStatic = null,
                PathSrc = null,
                PathByUrl = null,
                PathOutTemplate = null,
                AutoComplete = 'false',
                MainStaticPath = null
    ) {
        /*
        По умолчанию подразумевается следующая архитектура приложения

        - app
            - src (Место для исходных скриптов)
            - static
                - public (Место для скомпилированных статических файлов)
            - template (Место для html файла)
         */

        this.isDev = isDev;
        this.PathOutStatic = PathOutStatic ? PathOutStatic : path.resolve(PathApp, 'static');
        this.PathSrc = PathSrc ? PathSrc : path.resolve(PathApp, 'src');
        this.PathByUrl = PathByUrl ? PathByUrl : '/static/public';
        this.PathOutTemplate = PathOutTemplate ? PathOutTemplate : path.resolve(PathApp, 'templates')
        this.AutoComplete = AutoComplete === "true";
        this.MainStaticPath = MainStaticPath

        console.log(
            {
                "PathOutStatic": this.PathOutStatic,
                "PathSrc": this.PathSrc,
                "PathByUrl": this.PathByUrl,
                "PathOutTemplate": this.PathOutTemplate,
                "AutoComplete": this.AutoComplete,
                "MainStaticPath": this.MainStaticPath
            }
        )

        this.res = {
            // Следить за изменением файлов, и автоматически перекомпилировать их. Консоль блокируется на момент слежки
            // (true/false)
            watch: this.AutoComplete,

            // Режим работы [production(сжатие кода)/development]
            mode: isDev ? 'development' : 'production',

            // Вариант сборки https://webpack.js.org/configuration/devtool/
            devtool: this.DevTool(),

            // Путь для входных файлов
            entry: this.Entry(),

            // Путь для выходных файлов после компиляции
            output: this.Output(),

            // Оптимизировать импорты сторонних библиотек
            optimization: this.optimization(),

            // Файлы с каким расширением мы подключаем без указания расширения
            resolve: {
                extensions: ['.ts', '.tsx', '.js', '.svelte'],
                modules: [path.resolve(__dirname, 'node_modules'), 'node_modules'],
            },

            // Список используемых плагинов
            plugins: this.Plugins(),

            // Настройки для различных форматов файлов (предпроцессоры)
            module: {
                // конфигурация относительно модулей
                rules: [
                    /* Обработка импортов различных типов фалов */
                    //// JS
                    // this.JS_load(),
                    //// TS
                    // this.TS_load(),
                    // SVELTE
                    this.SVELTE_load(),
                    // CSS
                    this.CSS_load(),
                    // SASS-SCSS
                    this.SASS_load(),
                    // File
                    this.FILE_load(),
                    // Fonts
                    this.FONTS_load(),
                ],
            },

            // Настройка `webpack-dev-server`
            devServer: this.DevServer(),

            // Увеличить максимальный размер статических файлов
            performance: {
                hints: false,
                maxEntrypointSize: 512000,
                maxAssetSize: 512000,
            },
        };
    }

    // Настройка указывающая -> нужно ли создавать хешь в имени файлов
    filename(ext) {
        /* В режиме разработки хеш нам не нужно. Но когда мы отправляем в релиз файлы, то нам нужен
        хеш файлов, для того чтобы пользователи не кешировали устаревшие статические файлы, а загружали новые,
        это будет происходить потому что имена файлов будут разными.
        */
        return this.isDev
            ? `[name].bundle.${ext}`
            : `[name].[contenthash].${ext}`;
    }

    // Функция для настроек оптимизации (сжатия) файлов
    optimization() {
        // Оптимизировать импорты сторонних библиотек
        const conf = {
            splitChunks: {
                chunks: 'all',
            },
        };
        // Если не режим разработки то сжимаем `JS` и `CSS`
        if (!this.isDev) {
            conf.minimize = true;
            conf.minimizer = [
                new OptimizeCssAssetsPlugin(),
                new TerserPlugin(),
            ];
        }
        return conf;
    }

    // Функция для подключения плагинов
    Plugins() {
        let plug = [
            // Плагин для автоматического подключения статических файлов в `HTML` шаблон
            new HTMLWebpackPlugin({
                // Указать какой `HTML` шаблон взять за основу
                template: `${this.PathSrc}/index.template.html`,

                // Куда поместить итоговый `HTMl` файл
                filename: `${this.PathOutTemplate}/index.html`,

                // Оптимизировать сборку `HTMl`файла если не режим разработки
                minify: {
                    // Варианты: https://github.com/terser/html-minifier-terser#options-quick-reference
                    collapseWhitespace: !this.isDev,
                    keepClosingSlash: !this.isDev,
                    removeComments: !this.isDev,
                    removeRedundantAttributes: !this.isDev,
                    removeScriptTypeAttributes: !this.isDev,
                    removeStyleLinkTypeAttributes: !this.isDev,
                    useShortDoctype: !this.isDev,
                },

            }),
            // Удалять старые версии статических файлов из `output`
            new CleanWebpackPlugin(),
            // Создать общий `.css` файл со стилями
            new MiniCssExtractPlugin({
                filename: this.filename('css'),
            }),
            // // Копировать файлы или папки при сборки проекта
            // new CopyWebpackPlugin([
            //         // Копирование
            //         {
            //             // Откуда копировать
            //             from: path.resolve(__dirname,``),
            //             // Куда копировать
            //             to: path.resolve(__dirname,``)
            //         },
            //     ]
            // )

        ];
        // Если режим разработки, то показать размер статических файлов
        if (!this.isDev) {
            plug.push(new BundleAnalyzerPlugin());
        }
        // Если есть общая папка со всеми стати, и у нас стоит автокомпеляция, то
        // мы будем копировать имения статических файлов в главною директорию со статическими файлами
        if (this.MainStaticPath && this.AutoComplete) {
            plug.push(new CopyWebpackPlugin({
                    patterns: [
                        {from: this.PathOutStatic, to: this.MainStaticPath},
                    ],
                })
            )
        }
        return plug;
    }

    DevTool() {
        return this.isDev ? 'source-map' : false;
    }

    Entry() {
        return {
            // Его мы подключаем в `indexs.html`
            main: `${this.PathSrc}/main.js`,
            // Путь к другому файлу для компиляции
            // other: path.resolve(__dirname, `src/other.tsx`)
        };
    }

    Output() {
        return {
            // Имя выходного файла.
            // `name` возьмётся из ключа `entry`.
            // `contenthash` будет создавать хеш файла для индивидуальности
            filename: this.filename('js'),
            // Путь куда помещаются скомпилированные файлы
            path: this.PathOutStatic, // 127.0.0.1/static/frontend_react/public/ откуда подаются файлы
            // Путь который будет в html ссылке
            publicPath: `${this.PathByUrl}`,
        };
    }

    DevServer() {
        return {
            // Порт на котором будет запущен Лайф сервер
            port: 8011,
            devMiddleware: {
                // Записывать изменения в файл, а не в ОЗУ
                writeToDisk: true,
            },
            // Путь к статиечским файлам
            static: {
                directory: this.PathOutStatic,//path.join(__dirname, `${this.PathOutStatic}/`),
            },
            // Разрешить все домены
            allowedHosts: 'all',
            // Атоперезагрузка если режим разработки
            hot: this.isDev,
        };
    }

    SVELTE_load() {
        return {
            test: /\.svelte$/,
            use: {
                loader: 'svelte-loader',
            },
        };
    }

    JS_load() {
        return {};
    }

    TS_load() {
        return {
            // свойство определяет, какой файл или файлы следует преобразовать.
            test: /\.tsx|ts?$/,
            // Игнорирует папки [node_modules/, bower_components/]
            exclude: /(node_modules|bower_components)/,
            // какой загрузчик следует использовать для преобразования.
            use: 'ts-loader',
        };
    }

    CSS_load() {
        return {
            test: /\.css$/,
            // `css-loader` - поваляет импортировать `.css` в `js`
            // `style-loader` - подключает `.css` в `HTML` (Удален)
            // `MiniCssExtractPlugin`- создавать отдельный `.css` файл
            use: [
                // Настройки для `MiniCssExtractPlugin`
                {
                    loader: MiniCssExtractPlugin.loader,
                    options: {},
                },
                'css-loader',
            ],
        };
    }

    SASS_load() {
        return {
            test: /\.s[ac]ss$/,
            // `css-loader` - поваляет импортировать `.css` в `js`
            // `style-loader` - подключает  `.css` в `HTML` (Удален)
            // `MiniCssExtractPlugin` -  создавать отдельный `.css` файл
            use: [
                // Настройки для `MiniCssExtractPlugin`
                {
                    loader: MiniCssExtractPlugin.loader,
                    options: {},
                },
                'css-loader',
                'sass-loader',
            ],
        };
    }

    FONTS_load() {
        return {
            test: /\.(ttf|woff|woff2|eot)$/,
            use: ['file-loader'],
        };
    }

    FILE_load() {
        return {
            test: /\.(png|jpg|svg|gif|web)$/,
            use: ['file-loader'],
        };
    }
}

// Считываем переменные окружения из файла `npm install dotenv`
const envy = require('dotenv').config({path: './__env.env'});
// Получить режим разработки (bool)
const isDev = envy.parsed.DEBUG === 'true';
console.log('isDev:\t\t', isDev);

// npx webpack --config webpack.config.js --env PathOutStatic=./project_name/static/public/ --env PathSrc=./project_name/src/ --env PathByUrl=/static/public
// npm run build -- --env PathOutStatic=./project_name/static/public/ --env PathSrc=./project_name/src/ --env PathByUrl=/static/public
// npm run build -- --env PathOutStatic=./test_prog/static/public/ --env PathSrc=./test_prog/src/ --env PathByUrl=/static/pic

module.exports = (env) => {
    /*

    @params env: объект с переменными окружения. Для того чтобы передать из консоли используйте синтаксис
    --env $Ключ$=$Значение$.
    https://webpack.js.org/guides/environment-variables/

    */
    obj_ = new Main(isDev, env.PathApp,
        env.PathOutStatic,
        env.PathSrc,
        env.PathByUrl,
        env.PathOutTemplate,
        env.AutoComplete,
        env.MainStaticPath
    );
    console.log(obj_.res);
    return obj_.res;
};
