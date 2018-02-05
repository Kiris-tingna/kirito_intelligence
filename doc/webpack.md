webpack 从入门到工程实践

作者/分享人：zhangwang
本文较长，为了节省你的阅读时间，在文前列写作思路如下：

什么是webpack，它要解决的是什么问题？
对webpack的主要配置项进行分析，虽然不会涉及太多细节，但是期待在本节能让我们知晓如果我们有什么需求，我们该从哪些配置项着手修改？
分析create-react-app的基础配置文件。
分享一些自己工作中对webpack的实践。
本文的初衷是和你一起理清webpack的使用逻辑，以便能更加容易的编写及拓展自己项目所需的配置文件。不过也得提前说明本文可能并不是一篇好的可以跟着操作的教程（想跟着一步步做的童鞋可以看官方示例和webpack入门，看这篇就够了。

换个角度看待webpack

近年来，前端技术蓬勃发展，我们想在js更方便的实现html , 社区就出现了jsx,我们觉得原生的css不够好用，社区就提出了scss,less，针对前端项目越来越强的模块化开发需求，社区出现了AMD,CommonJS,ES2015 import等等方案。遗憾的是，这些方案大多并不直接被浏览器支持，往往伴随这些方案而生的还有另外一些，让这些新技术应用于浏览器的方案，我们用babel来转换下一代的js，转换jsx;我们用各种工具转换scss,less为css；我们发现项目越来越复杂，代码体积越来越大，又要开始寻找各种优化，压缩，分割方案。前端工程化这个过程，真是让我们大费精力。我们也大多是在寻找前端模块化解决方案的过程中知晓了webpack。

的确，webpack的流行得益于野性生长的前端，其本质是一种前端模块化打包解决方案，但是更重要的是它又是一个可以融合运用各种前端新技术的平台，明白webpack的使用哲学后，只需要简单的配置,我们就可以随心所欲的在webpack项目中使用jsx/ts,使用babel/postcss等平台提供的众多其它功能，只需通过一条命令由源码构建最终可用文件。可以不夸张的说webpack为前端的工程化开发提供了一套相对容易和完整的解决方案。一些知名的脚手架工具，也大多基于webpack(比如create-react-app)。

webpack好难！我第一次复制别人的配置文件到我的项目中，发现以自己仅有的JS知识完全看不懂时，也有这种感觉。后来发现有这种感觉其实是因为自己看待webpack的角度错了，对大多数前端开发者而言，以往我们接触的各种库，要么类似jQuery,通过$符在前端项目中直接运行，所做的事情只在前端生效，要么类似express.js,在node.js项目中直接require后就可以使用，所做的事情只在后端生效。webpack的不同之处就在于，虽然我们的配置文件位于前端项目中，但实际上它却运行于node.js，之后的处理结果又供前端使用（也可能供node使用）。所以学习之前，我们转变一下思维，从node.js的角度来看webpack，很多事情就会简单起来。

我们对下图一定不陌生，假设现在我们手中有一系列相互关联的文件js,jsx,css,less,jpg，我们一步步的看看为了把它们转换为项目最终需要的，浏览器可识别的文件，webpack都做了什么。

webpack做了什么

对webpack主要配置项的分析

如果不去考究细节，我们大可把webpack简化理解为一个函数，配置文件则是其参数，传入合理的参数后，运行函数就能得到我们想要的结果。

webpack也只是一个打包工具，它可不是什么智能ai，我们该从哪儿输入文件，我们想把输出结果放哪里，输出结果应该长什么样，它都不知道。而我们目前和webpack函数交互的唯一方法就是通过参数，这就涉及到webpack配置对象中两个重要概念entry和output了，因此，我们的配置对象至少具备以下结构：

// 第一阶段
{
    entry:{},
    output:{}
}
入口配置entry

理想状态是，我们把所有自己编写的文件都交给webpack,让它找明里面的关系，进过一定处理后，给出最终我们想要的结果。遗憾的是，webpack也不会机械学习，我们手头的一堆文件之间的关系是自己确定的，一般我们的项目都会存在一个或几个主文件，其它的所有的文件（模块）都直接或间接的链接到了这些文件。我们在entry项中需要填写的就是这些主文件的信息。

不过我们也不要嫌弃webpack笨，通过我们给的主文件路径，通过分析它能构建最合适的依赖关系，这意味着只有用过的代码才会被打包，比如我们在一个文件中写了五个模块，但是实际只用了其中一个，打包后的代码只会包含引用过的模块。

webpack中很多地方的配置都有多种写法，这也是其让人疑惑的地方之一，很遗憾，我们的第一个配置对象entry就是如此。

entry可以是三种值：

字符串:如entry:'./src/index.js'，字符串也可以是函数的返回值，如entry: () => './demo'，单一入口占位符[name]值为main（关于占位符，稍后详述）；

数组形式，如[react,react-dom]，可以把数组中的多个文件打包转换为一个chunk；

对象形式，如果我们需要配置的是多页应用，或者我们要抽离出指定的模块做为公共代码，就需要采用这种形式了，属性名是占位符[name]的值，属性值可以是上面的字符串和数组，如下:

// 值得注意的是入口文件有几个就会生成几个独立的依赖图谱。
entry:{
    main:'./src/index.js',
    second:'./src/index2.js',
    vendor: ['react','react-dom']
}
好吧，千辛万苦，我们在一堆各种类型的文件中找到了入口文件，这里我们假设为./src/index.js，此时我们的配置对象如下：

// 第二阶段
{
    entry:{
        main:'./src/index.js'
    },
    output:{}
}
webpack依据入口文件来构建依赖体系，每个入口文件在打包完成后都具备其独立的依赖图谱，在此我们暂时称这些由主入口配置生成的文件为主js文件。
输出配置output

output配置项作用于打包文件的输出阶段，其作用在于告知webpack以何种方式输出打包文件，关于output，webpack提供了众多的可配置选项，我们简单介绍下最常用的选项。

output基本配置项

我们都另存过文件，当我们另存一个文件时，我们需要确定另存的文件名和另存的路径，webpack将打包后的结果导出的过程就类似于此，此过程由output配置项控制，其最基本配置包括filename和path两项。这两项用以决定上述主js文件的存储行为。

不过我们程序的首页往往不需用到某个主js文件的所有代码，实际开发中，我们常常使用一定方法对代码进行分割，方便按需加载，提升体验。这类不具备独立依赖的文件，我们称之为chunkfile。chunkfile的命名，在output中对应chunkFilename项；

此外output的publicPath项，用于控制打包文件的相对或者绝对引用路径，配置不当往往造成在运行时找不到文件。

我们补充配置对象中output的配置，如下：
```
// 第三阶段
{
    entry:{
        main:'./src/index.js'
    },
    output:{
        path: path.join(__dirname,'./dist'),
        name:'js/bundle-[name]-[hash].js',
        chunkFilename:'js/[name].chunk.js',
        publicPath:'/dist/'
    }
}
```
上述代码中用到了占位符[name]，我们对占位符做统一解释：

webpack中常见的占位符有多种，常见的如下：

[name]:代表打包后文件的名称，在entry或代码中(之后会看到)确定；
[id]:webpack给块分配的内部chunk id，如果你没有隐藏，你能在打包后的命令行中看到；
[hash]：每次构建过程中，生成的唯一 hash 值;
[chunkhash]: 依据于打包生成文件内容的 hash 值,内容不变，值不变；
[ext]: 资源扩展名,如js,jsx,png等等;
output其它配置

output配置项生效于保存这个过程，除了上面的基本配置，如果你想对这个阶段的打包文件进行更改，都可在此配置项中进行相关设置。

比如output提供了众多关于hash的属性，让我们对[hash]占位符的值有更加精细的控制，如生成方式，使用的算法，预设的长度等等；如chunkLoadTimeout属性则允许我们设置chunk文件的请求超时时间。

工具都是依赖于需求来使用的，如果你此阶段有别的需求，可点击更多配置寻找解决方案。

我们已经知道了webpack中基本的输入和输出配置，但是webpack对各模块的处理过程，目前为止，对我们还是一个谜。考虑到webpack执行于node.js环境，其本身只能理解js文件，而我们输入的却是一大堆不同格式的文件，毫无疑问,要做的第一件事情是对各类模块进行处理，这就涉及到webpack中第三个重要配置对象了---module。

对模块的处理：module的配置

使用webpack时，我们常常听说，对webpack而言，所有的文件都是模块，前文中我也常常混用模块和文件，不过本质上模块和文件还是不同的，webpack里，文件可以当做模块，而模块却不一定是一个独立的文件。我们先看看webpack内置支持的模块类型：

ES2015 import（webpack2开始内置支持）。

CommonJS require。

AMD define和require语句。

css/less/sass 中的@import。

样式中的url(...)和html文件中的<img src="..."/>。

我们知道webpack只能处理js文件，我们的浏览器也可能不支持一些最新的js语法，基于此，我们需要对传入的模块进行一定的预处理，这就涉及到webpack的又一核心概念 --- loader，使用loader，webpack允许我们打包任何JS之外的静态资源。

loader的作用和基本用法

webpack中，loader的配置主要在module.rules中进行，module.rules是一个数组，我们可以把每一项看做一个Rule，每个Rule主要做了以下两件事：

识别文件类型，以确定具体处理该数据的loader，（Rule.test属性）。

使用相关loader对文件进行相应的操作转换，（Rule.use属性）。

还记得前面我们说过，我们手头的文件类型有js,jsx,css,less,jpg吗？我们看看在webpack中该如何处理和转换它们。

注：以下loader使用前需通过npm/cnpm/yarn安装：
```
module: {
   rules: [{
       test: /(\.jsx|\.js)$/,
       use: {
           loader: "babel-loader",
           options: {
               presets: ["es2015", "react"]
           }
       },
       exclude: /node_modules/
   }, {
       test: /\.css$/,
       use: ["style-loader", "css-loader"]
   }, {
       test: /\.less$/,
       use: ["style-loader", "css-loader", "less-loader"]
   }]
},
```
这就是webpack中loader的基本用法了，在module.rules数组中进行配置即可，module.rules是一个数组，里面每一项（一个Rule）表示以一定的规则匹配和处理某种或某几种类型的文件。具体说来：

Rule.test:表示匹配规则，它是一个正则表达式。

Rule.use:表示针对匹配的文件将使用的处理loader，其值可以是字符串，数组和对象，当是对象形式时，我们可以使用options等命令进行进一步的配置。

Rule中的其它一些规则也大多围绕匹配条件和应用结果展开，如Rule.exclude和Rule.include表示应该匹配或不应该匹配某资源；Rule.oneOf表示对该资源只应用第一个匹配的loader；Rule.enforce则用于指定loader的种类。

loader可以做什么

webpack的强大之处在于，可以轻松在其中应用其它平台提供的功能，比如说babel,postcss本身都是独立的平台。在webpack中只需要添加babel-loader和postcss-loader就可以使用。这两个平台本身也提供众多的配置项，默认分别可在.babelrc 和postcss.config.js中完成，webpack并不影响这些配置文件的使用。不过需要说明的可能很多童鞋是在学习webpack时才接触这两个平台，导致在这两个平台上遇到的问题误以为是webpack的问题。
除了上述的转换编译，通过loader，webpack还允许我们实现以下功能：

转换编译：script-loader/babel-loader/ts-loader/coffee-loader等。

处理样式：style-loader/css-loader/less-loader/sass-loader/postcss-loader等。

处理文件：raw-loader/url-loader/file-loader/等。

处理数据：csv-loader/xml-loader等。

处理模板语言：html-loader/pug-loader/jade-loader/markdown-loader等。

清理和测试：mocha-loader/eslint-loader等。

关于各个loader更详细的介绍，可点击loaders查看。

module.noParse

关于module，另一个常用的配置项为module.noParse，通过它，我们在构建过程中可以忽略大型的 library 以提高构建效率。

我们来整理一下此阶段，我们的配置对象代码，如下：
```
// 第四阶段
{
    entry: {
        main: './src/index.js'
    },
    output: {
        path: path.join(__dirname, './dist'),
        name: 'js/bundle-[name].js',
        chunkFilename: 'js/[name].chunk.js',
        publicPath: '/dist/'
    },
    module: {
        rules: [{
            test: /(\.jsx|\.js)$/,
            use: {
                loader: "babel-loader",
                options: {
                    presets: ["es2015", "react"]
                }
            },
            exclude: /node_modules/
        }, {
            test: /\.css$/,
            use: ["style-loader", "css-loader"]
        }, {
            test: /\.less$/,
            use: ["style-loader", "css-loader", "less-loader"]
        }]
    }
}
```
进过这一阶段的处理，我们的代码其实已经可以输出使用了。不过这样的输出可能还不能让人满意，我们想要抽离公共代码；我们想统一修改所有代码中的某些值；我们还想对代码进行压缩，去除所有的console… , 总之这一阶段的代码还是存在很大的改进空间的，这就是plugin的用武之地了。

plugins的配置

webpack称plugins为其backbone,一切loader不能做的处理都可由plugins来做。此评价足见其重要性。

鉴于插件如此重要，webpack内置了众多的常用的plugins，无需额外安装就可直接使用。我们先看看plugins的基本配置方法，然后再分类介绍一下常用的plugins。

plugins的使用方法

plugins是一个数组，数组中的每一项都是某一个plugin的实例，plugins数组甚至可以存在一个插件的多个实例。

下面代码中，分别展示了webpack内置插件和第三方插件的使用方法：
```
// 第三方插件需要在安装后引入
const CleanWebpackPlugin = require("clean-webpack-plugin");

{
    ...
    plugins:[
      new webpack.DefinePlugin({
        "process.env": {
            NODE_ENV: JSON.stringify("production")
        }
    }),
      new CleanWebpackPlugin(["js"], {
        root: __dirname + "/stu/",
        verbose: true,
        dry: false
    })
    ]
}
```
一种插件其实就是一种函数，通过传入不同的参数，插件可按我们的需求实现不同的功能。不过插件数量众多，我们甚至还可以自己来写插件，每个插件还有自己特定的配置规则，这也是webpack让人觉得难学的地方之一，不过好在作为一个工具，对于我们大多数人最需要掌握的plugins并不是那么多，其它的待真的有相关需求再边查边学也不迟，webpack的插件列表可参看这里。

常用plugins的介绍

plugins功能众多，但是大多数plugin的功能主要集中在两方面：

对前一阶段打包后的代码进行处理，如添加替换一些内容，分割代码为多块，添加一些全局设置等。

辅助输出，如自动生成带有链接的index.html，对生成文件存储文件夹做一定的清理等。

对代码进行处理

BannerPlugin:给代码添加版权信息，如在plugins数组中添加new BannerPlugin(‘GitChat’)后能在打包生成的所有文件前添加注释GitChat详见。

CommonsChunkPlugin，用于抽离代码，具有多种用途 详情查看CommonsChunkPlugin。

抽离不同文件的共享代码，减少chunk间的重复代码，有效利用缓存。

抽离可能整个项目都在使用的第三方模块，比如react react-dom。

将多个子chunk中的共用代码打包进父chunk或使用异步加载的单独chunk。

抽离Manifest这类每次打包都会变化的内容，减轻打包时候的压力，提升构建速度。

CompressionWebpackPlugin:使用配置的算法（如gzip）压缩打包生成的文件，详见。

DefinePlugin:创建一个在编译时可配置的全局常量,如果你自定义了一个全局变量PRODUCTION,可在此设置其值来区分开发还是生产环境详见。

EnvironmentPlugin:实际上是DefinePlugin插件中对process.env进行设置的简写形式，如new webpack.EnvironmentPlugin(['NODE_ENV', 'DEBUG'])将设置process.env.NODE_ENV='DEBUG',EnvironmentPlugin。

ExtractTextWebpackPlugin:抽离css文件为单独的css文件，详见。

ProvidePlugin：全局自动加载模块，如添加new webpack.ProvidePlugin({$: 'jquery', jQuery: 'jquery'})后,则全局不用在导入jquery就可以直接使用$，ProvidePlugin。

UglifyjsWebpackPlugin:使用前需要先安装，基于UglifyJS压缩代码，支持其所有配置UglifyjsWebpackPlugin。

辅助输出打包后的代码

HtmlWebpackPlugin:使用前需要先安装，为你自动生成一个html文件，该文件将自动依据entry的配置引入依赖，如果你的文件名中添加了[hash]等占位符，这将非常有用, 详见。

CleanWebpackPlugin:使用前需要先安装，此插件允许你在配置以后，每次打包时，清空所配置的文件夹，如果你每次打包的文件名不同，这将非常有用 GitHub - clean-webpack-plugin。

通过上述对不同插件的描述，你一定大致明白了，插件可以做什么，之后在开发的过程中，如果你遇到的什么需要在此阶段解决的问题，大可搜索看看是否有相关的插件，推荐查阅awesome-webpack。

学习了插件以后，现在我们的配置对象是如下这样：
```
// 第5阶段
{
    entry: {
        main: './src/index.js'
    },
    output: {
        path: path.join(__dirname, './dist'),
        name: 'js/bundle-[name].js',
        chunkFilename: 'js/[name].chunk.js',
        publicPath: '/dist/'
    },
    module: {
        rules: [{
            test: /(\.jsx|\.js)$/,
            use: {
                loader: "babel-loader",
                options: {
                    presets: ["es2015", "react"]
                }
            },
            exclude: /node_modules/
        }, {
            test: /\.css$/,
            use: ["style-loader", "css-loader"]
        }, {
            test: /\.less$/,
            use: ["style-loader", "css-loader", "less-loader"]
        }]
    },
    plugins: [
        new webpack
        .optimize
        .CommonsChunkPlugin({
            name: 'vendor',
            filename: "js/[name]-[chunkhash].js"
        }),
        new webpack.optimize.CommonsChunkPlugin({
            name: "manifest",
            minChunks: Infinity
        }),
        new webpack.ProvidePlugin({
            Promise: "exports-loader?global.Promise!es6-promise",
            fetch: "exports-loader?self.fetch!whatwg-fetch"
        }),
        new HtmlWebpackPlugin({
            filename: "index.html",
            template: "app/index.html",
            inject: "body"
        }),
        new CleanWebpackPlugin(["js"], {
            root: __dirname + "/stu/",
            verbose: true,
            dry: false
        }),
        new webpack.DefinePlugin({
            "process.env": {
                NODE_ENV: JSON.stringify("production")
            }
        })
    ]
}
```
至此，从输入entry->处理loaders/plugins->输出output，我们讲解了webpack的核心功能，不过webpack还提供其它的一些配置项，这些配置项大多从两方面起作用，辅助开发、对构建过程中的一些细节做调整。对这些属性，下面只做简单的介绍。

其它的一些配置

辅助开发的相关属性

devtool:

打包后的代码和原始的代码往往存在较大的差异，此选项控制是否生成，以及如何生成 source map，用以帮助你进行调试，详情可查看Devtool。

devServer：

通过配置devServer选项，你可以开启一个本地服务器，webpack为此本地服务器提供了非常多的配置选项，点击查看dev-server，你会发现通过合适的配置，你可以拥有所有本地服务器可提供的功能。

watch:

启用 Watch 模式后，webpack 将持续监听任何已解析文件的更改，重新构建文件，Watch 模式默认关闭，在开发时候如果开启会很方便。

watchOptions:

一组用来定制 Watch 模式的选项： 详见 watch。

performance:

本配置让你设置打包后命令行中该如何展示性能提示，比如是否开启提示，资源如果超过某个大小时该警告还是报错，详见performance。

stats:

本选项让你配置打包过程中输出的内容，如没有输出none，标准输出normal，全部输出verbose，只输出错误errors-only等等。

精细配置相关属性

content:设置基础路径，默认使用当前目录。

resolve:

确定模块如何被解析，webpack已经提供了合理的默认值，不过通过你的自定义配置，可以对模块解析实现更加精细的控制，如对某些常用模块可以通过设置别名以更容易引用，也可在此处设置可被忽略的后缀名，详见 resolve。

target:

告知 webpack 需要打包的代码执行的环境，针对 node 和 web 打包过程会有所不同，详见Target。

externals:

让打包生成的代码中不添加某依赖项，而让这些依赖项直接从用户环境中获取,在进行库的开发时非常有用。

node:

是一个对象，其中每个属性都是 Node.js 全局变量或模块的名称,每一项的设置值都可以是（true/mock/empty/false）中的一种，以确定这些node中的对象在其它环境中是否可用。

此外webpack还具备其它一些用的比较少的配置对象，详见 Other Options。

至此，我们了解了webpack常用的配置项及其意义。为了检测我们的学习成果，我们一起分析一个中等项目中的webpack配置文件。配置文件来自于create-react-app,使用create-react-app新建项目后，执行npm run eject可看到多个配置文件，这里我们选择webpack.dev.js。

分析create-react-app中webpack的配置
```
const path = require('path');
const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const CaseSensitivePathsPlugin = require('case-sensitive-paths-webpack-plugin');
const InterpolateHtmlPlugin = require('react-dev-utils/InterpolateHtmlPlugin');
const WatchMissingNodeModulesPlugin = require('react-dev-utils/WatchMissingNodeModulesPlugin');
const eslintFormatter = require('react-dev-utils/eslintFormatter');
const ModuleScopePlugin = require('react-dev-utils/ModuleScopePlugin');

module.exports = {
  devtool: 'cheap-module-source-map',
  entry: [
    require.resolve('react-dev-utils/webpackHotDevClient'),
    require.resolve('./polyfills'),
    require.resolve('react-error-overlay'),
    'src/index.js'
  ],
  output: {
    path: '/build/',
    pathinfo: true,
    filename: 'static/js/bundle.js',
    chunkFilename: 'static/js/[name].chunk.js',
    publicPath: '',
    devtoolModuleFilenameTemplate: info =>
      path.resolve(info.absoluteResourcePath).replace(/\\/g, '/'),
  },
  resolve: {
    modules: ['node_modules'],
    extensions: ['.web.js', '.js', '.json', '.web.jsx', '.jsx'],
    alias: {
      'react-native': 'react-native-web',
    },
    plugins: [
      new ModuleScopePlugin('/src'),
    ],
  },
  module: {
    strictExportPresence: true,
    rules: [{
      test: /\.(js|jsx)$/,
      enforce: 'pre',
      use: [{
        options: {
          formatter: eslintFormatter,
        },
        loader: require.resolve('eslint-loader'),
      }, ],
      include: 'src',
    }, {
      exclude: [/\.html$/,/\.(js|jsx)$/,/\.css$/,/\.json$/,/\.bmp$/,/\.gif$/,/\.jpe?g$/,/\.png$/],
      loader: require.resolve('file-loader'),
      options: {
        name: 'static/media/[name].[hash:8].[ext]',
      },
    }, {
      test: [/\.bmp$/, /\.gif$/, /\.jpe?g$/, /\.png$/],
      loader: require.resolve('url-loader'),
      options: {
        limit: 10000,
        name: 'static/media/[name].[hash:8].[ext]',
      },
    }, {
      test: /\.(js|jsx)$/,
      include: 'src',
      loader: require.resolve('babel-loader'),
      options: {
        cacheDirectory: true,
      },
    }, {
      test: /\.css$/,
      use: [
        require.resolve('style-loader'), {
          loader: require.resolve('css-loader'),
          options: {
            importLoaders: 1,
          },
        }, {
          loader: require.resolve('postcss-loader'),
          options: {
                    ...
          },
        },
      ],
    }, ],
  },
  plugins: [
    new InterpolateHtmlPlugin({
      NODE_ENV:'development',
      PUBLIC_URL:''
    }),
    new HtmlWebpackPlugin({
      inject: true,
      template: 'public/index.html',
    }),
    new webpack.NamedModulesPlugin(),
    new webpack.DefinePlugin({
      'process.env':{
        NODE_ENV:"development",
        PUBLIC_URL:'" "'
      }
    }),
    new webpack.HotModuleReplacementPlugin(),
    new CaseSensitivePathsPlugin(),
    new WatchMissingNodeModulesPlugin(paths.appNodeModules),
    new webpack.IgnorePlugin(/^\.\/locale$/, /moment$/),
  ],
  node: {
    dgram: 'empty',
    fs: 'empty',
    net: 'empty',
    tls: 'empty',
  },
  performance: {
    hints: false,
  },
};
```
对可能和你看到的webpack.config.dev.js有所不同的说明：：

npm run reject之前，对create-react-app的一些设置会影响这里看到的配置文件。

原始的webpack.config.dev.js中，部分值由外部函数生成，相关值，在上述代码中直接改为了确定的结果，如env.raw在上述代码中被替换为：

{
      NODE_ENV:'development',
      PUBLIC_URL:''
    }
create-react-app在开发环境并不生成真实的文件到硬盘，上述代码中的部分路径可能有误，见谅。

推荐在看下面的分析前，花三分钟看看上述文件，如果都能看得懂，那么恭喜你，你已经明白webpack的运作方式了，快去自己的项目中实践吧，如果还有疑惑，也不要紧，我们一起来分析。

webpack.config.dev.js执行于node环境

首先，我们应该明确webpack.config.dev.js执行于node环境,目的在于返回webpack需要的配置对象，因此其中可以使用node提供的一些特殊变量和语法，比如__dirname，又如引入模块时采用CommonJS模式。

此文件的开头，首先通过require语句引入了path,webpack和一系列webpack插件，除了HtmlWebpackPlugin在前文中我们见过，其它的我们都未曾见过，其实这些大多是create-react-app针对webpack已有的插件改进或新开发的插件，所以不熟悉也正常，随后我们将一个个的弄清楚它们是干嘛的。

对module.exports的分析

devtool

此处的配置值为cheap-module-source-map,代表不带列映射的 SourceMap，将加载的 Source Map 简化为每行单独映射。

entry

此处的entry是一个数组，代表着四项的代码都会添加到打包结果之中。

webpackHotDevClient可以被看做具有更好体验的WebpackDevServer。

./ployfill.js用以在浏览器中支持promise/fetch/object-assign。

react-error-overlay在开发环境中使用，强制显示错误页面。

./src/index.js则是我们的app的主入口。

output

在实际使用create-react-app的过程中，我们并看不见开发环境的打包结果，因此此处的说明仅供参考。

path指定，打包后文件存放的位置为/build/。

pathinfo为true，在打包文件后，在其中所包含引用模块的信息，这在开发环境中有利于调试。

filename指定了打包的名字和基本的引用路径static/js/bundle.js。

chunkFilename:指定了非入口文件的名称static/js/[name].chunk.js。

publicPath:指定服务器读取时的路径，此处设置为。

devtoolModuleFilenameTemplate:这里是一个函数，指定了map位于磁盘的位置。

resolve

modules:指定了模块的搜索的位置，这里设置为node_modules。

extensions:指明在引用模块时哪些后缀名可以忽略，这里忽略的文件名包括.js/.jsx/.web.js/.web.jsx等。

alias:创建 import 或 require 的别名，使得部分模块的引用变得简单，安装上文的设置，现在我们可以直接引用react-native和react-native-web了。

plugins:此处使用了ModuleScopePlugin的实例，用以限制自己编写的模块只能从src目录中引入。

modules

strictExportPresence:这里设置为true,表明文件中如果缺少exports时会直接报错而不是警告。

rules：

Rule1：对js/jsx文件前置使用eslintFormatter，设置formatter格式为eslintFormatter。

Rule2：对exclude中的众多文件类型不使用file-loader,并设置其它文件打包后的名称按'static/media/[name].[hash:8].[ext]'格式设置。

Rule3: 对js/jsx文件调用babel-loader处理转换。

Rule4: 对css文件，按顺序调用style-loader,css-loader,postcss-loader进行处理。

##plugins

这里的一些插件，有的可能我们还比较陌生，我们一一介绍。
```
InterpolateHtmlPlugin:和HtmlWebpackPlugin串行使用，允许在index.html中添加变量。

HtmlWebpackPlugin:自动生成带有入口文件引用的index.html。

NamedModulesPlugin:当开启 HMR 的时候使用该插件会显示模块的相对路径，建议用于开发环境。

DefinePlugin:这里我们设置了process.env.NODE_ENV的值为development。

HotModuleReplacementPlugin:启用模块热替换。

CaseSensitivePathsPlugin:如果路径有误则直接报错。

WatchMissingNodeModulesPlugin:此插件允许你安装库后自动重新构建打包文件。

new webpack.IgnorePlugin(/^\.\/locale$/, /moment$/):忽略所匹配的moment.js。

node

设置node的dgram/fs/let/tls模块的的值，如果在其它环境中使用时值为empty。

performance

hints: false:不提示测试环境的打包结果。
```
上文一直讨论的是，webpack各设置项的基本意义，目的在于让你在有相关需求时，能知道该从哪一项下手查询。不过看到这里，如果你之前从未上手操作过webpack可能依旧不知道该如何使用，下面我分析一下，我在自己的项目中是如何使用的。

一些工程实践建议

官方文档的guides部分已经就如何实践提出了较多的建议，建议阅读以下内容前先行阅读。

结合npm使用

webpack在安装后有多种调用方法。

在命令行中直接传入参数使用（这个实际我用的比较少）。

自定义 webpack.config.js文件,在其中完成配置，然后在命令行中执行webpack --config webpack.config.js来使用，配置文件可以是任何其它名称（如果是webpack.config.js,我们直接使用webpack命令）。

结合npm使用，在package.json文件中的scripts对象中添加相关命令使用，之后通过npm run使用，如下：
```
"scripts": {
    "build:prod": "webpack --progress --colors --watch --config webpack.prod.js",
    "build:dev": "webpack --progress --colors --watch --config webpack.dev.js"
}
```
上面我们分别构建了webpack.prod.js和webpack.dev.js来分别生成开发环境和生产环境的代码，在命令行中执行npm run build:prod和npm run build:dev即可生成对应代码。

为生产环境指定合理的缓存

关于缓存，官方文档中有一节讲解的非常详细，请参见缓存。

合理分割代码

webpack提供了三种分割代码的方法，分别是通过entry,通过CommonsChunkPlugin插件和通过动态import（在webpack1.x中时也常常使用require.ensure来依据路由分割代码）。

entry的配置常用于多页应用，CommonsChunkPlugin的使用前文已做简要叙述，下面简单叙述下代码分割原则及我实际工作中是如何使用动态import来分割代码的。

分割原则

目前工作中主要依据两个原则来分隔代码：

前端路由：依据路由对应的页面进行分割，这种分割之后的体验类似于小程序中每次打开新页加载对应页面的js文件。

针对逻辑交互比较复杂的页面，如果某个较复杂的组件需被某操作触发后才呈现，也会把该组件分割出来。

分割方法

我们知道动态import返回值其实是一个Promise,基于此，对应于我用的React，我常采用以下函数辅助加载。
```js
// lib.js 定义懒加载函数
module.exports.withLazyLoading = function withLazyLoading(getComponent,Spinner = null) {
    return class LazyLoadingWrapper extends React.Component {
        constructor(props) {
            super(props);
            this.state = ({
                Component: null,
            })
        }

        componentWillMount() {
            const {onLoadingStart, onLoadingEnd, onError} = this.props;
              onLoadingStart();
            getComponent()
                .then(esModule => {
                    this.setState({Component: esModule.default})
                })
                .catch(err => {
                    onError(err, this.props)
                })
        }

        render() {
            const {Component} = this.state;
            if (!Component) return Spinner;
            return <Component {...this.props} />
        }
    }
};
```
对代码的分割方法如下：
```js
// 在需要的地方调用懒加载函数
import {withLazyLoading} from "lib";
// 
import {Loading} from 'Loadings';

export default withLazyLoading(
    () => {
        return import (/* webpackChunkName: "ConCard" */ "../../containers/ConCard.js")
    }, Loading());
```
简要的说明一下上述代码的意义，懒加载函数withLazyLoading接受动态import的组件和一个加载动画作为参数，动态import的组件加载成功前显示加载动画组件，成功后显示import的组件，通过自定义各种各样的Spinner加载动画，我们可以实现优雅的js文件加载过程。

观察打包后文件的结构，合理进行优化

使用webpack --json > stats.json命令可以生成一个包含依赖关系的json文件。webpack提供了多种可视化工具帮我们分析这个文件，我最喜欢的工具插件是BundleAnalyzerPlugin，可通过下述方法引入该插件：
```
new BundleAnalyzerPlugin({
    analyzerMode: 'static'
})
```
添加此插件，再次构建完成时，浏览器中将自动打开一个类似下面这样的网页：

BundleAnalyzerPlugin

这样我们可以轻易分析我们的代码分割是否合理，比如：

分割后文件过大的主要原因是在于引入了那些模块。

分析大多后的多文件中存不存在对某些比较大的模块的重复引用，方便我们进一步修正自己的配置文件。

上图是我之前项目中的一张截图，第一次见到这张图时还是给了我很多后期优化的思路的，引用chat.js的同时引入了moment.js,而实际上该页面只有一张图表，这让我考虑另寻图表解决方案，lodash,velocity在最初的项目中使用过，后逐步去除，属于遗留代码，现在还存在说明在局部可能还是用到了，这都是之后编码的改进方向。

##后记

总觉得技术类的文章也是该有生命力的，花了好久写完本文，回头看发现有的内容还是没有表达或交待清楚。所以有任何建议，请随意提出，我们在Chat中继续讨论，我也将对本文做长期持续的修改。

针对webpack3.5.5官网文档，使用mindNode制作了一个思维导图的草稿，此思维导图还需完善，之后将持续修改，点击此处可查看，该思维导图示例如下。

思维导图局部示例

另外，关于webpack1和webapck2的区别，官方文档中有一部分做了详细的讲解，所以本文中不做赘述，看完以后如果还有疑问，之后我们再详细讨论。



---
title: Migrating Versions
sort: 15
contributors:
  - sokra
  - jhnns
  - grgur
  - domfarolino
  - johnnyreilly
  - jouni-kantola
  - frederikprijck
  - chrisVillanueva
  - bebraw
  - howdy39
  - selbekk
  - ndelangen
---

The following sections describe the major changes from webpack 1 to 2.

T> Note that there were far fewer changes between 2 and 3, so that migration shouldn't be too bad. If you are running into issues, please see [the changelog](https://github.com/webpack/webpack/releases) for details.

W> This content may be moved to the blog post in the near future as version 2 has been out for a while. On top of that, version 3 was recently released and version 4 is on the horizon. As noted above, folks should instead to refer to [the changelog](https://github.com/webpack/webpack/releases) for migrations.


## `resolve.root`, `resolve.fallback`, `resolve.modulesDirectories`

These options were replaced by a single option `resolve.modules`. See [resolving](/configuration/resolve) for more usage.

``` diff
  resolve: {
-   root: path.join(__dirname, "src")
+   modules: [
+     path.join(__dirname, "src"),
+     "node_modules"
+   ]
  }
```


## `resolve.extensions`

This option no longer requires passing an empty string. This behavior was moved to `resolve.enforceExtension`. See [resolving](/configuration/resolve) for more usage.


## `resolve.*`

Several APIs were changed here. Not listed in detail as it's not commonly used. See [resolving](/configuration/resolve) for details.


## `module.loaders` is now `module.rules`

The old loader configuration was superseded by a more powerful rules system, which allows configuration of loaders and more.
For compatibility reasons, the old `module.loaders` syntax is still valid and the old names are parsed.
The new naming conventions are easier to understand and are a good reason to upgrade the configuration to using `module.rules`.

``` diff
  module: {
-   loaders: [
+   rules: [
      {
        test: /\.css$/,
-       loaders: [
-         "style-loader",
-         "css-loader?modules=true"
+       use: [
+         {
+           loader: "style-loader"
+         },
+         {
+           loader: "css-loader",
+           options: {
+             modules: true
+           }
+         }
        ]
      },
      {
        test: /\.jsx$/,
        loader: "babel-loader", // Do not use "use" here
        options: {
          // ...
        }
      }
    ]
  }
```


## Chaining loaders

Like in webpack 1, loaders can be chained to pass results from loader to loader. Using the [rule.use](/configuration/module#rule-use)
 configuration option, `use` can be set to an array of loaders.
In webpack 1, loaders were commonly chained with `!`. This style is only supported using the legacy option `module.loaders`.

``` diff
  module: {
-   loaders: [{
+   rules: [{
      test: /\.less$/,
-     loader: "style-loader!css-loader!less-loader"
+     use: [
+       "style-loader",
+       "css-loader",
+       "less-loader"
+     ]
    }]
  }
```


## Automatic `-loader` module name extension removed

It is not possible anymore to omit the `-loader` extension when referencing loaders:

``` diff
  module: {
    rules: [
      {
        use: [
-         "style",
+         "style-loader",
-         "css",
+         "css-loader",
-         "less",
+         "less-loader",
        ]
      }
    ]
  }
```

You can still opt-in to the old behavior with the `resolveLoader.moduleExtensions` configuration option, but this is not recommended.

``` diff
+ resolveLoader: {
+   moduleExtensions: ["-loader"]
+ }
```

See [#2986](https://github.com/webpack/webpack/issues/2986) for the reason behind this change.


## `json-loader` is not required anymore

When no loader has been configured for a JSON file, webpack will automatically try to load the JSON
file with the [`json-loader`](https://github.com/webpack/json-loader).

``` diff
  module: {
    rules: [
-     {
-       test: /\.json/,
-       loader: "json-loader"
-     }
    ]
  }
```

[We decided to do this](https://github.com/webpack/webpack/issues/3363) in order to iron out environment differences
  between webpack, node.js and browserify.


## Loaders in configuration resolve relative to context

In __webpack 1__, configured loaders resolve relative to the matched file. However, in __webpack 2__, configured loaders resolve relative to the `context` option.

This solves some problems with duplicate modules caused by loaders when using `npm link` or referencing modules outside of the `context`.

You may remove some hacks to work around this:

``` diff
  module: {
    rules: [
      {
        // ...
-       loader: require.resolve("my-loader")
+       loader: "my-loader"
      }
    ]
  },
  resolveLoader: {
-   root: path.resolve(__dirname, "node_modules")
  }
```


## `module.preLoaders` and `module.postLoaders` were removed:

``` diff
  module: {
-   preLoaders: [
+   rules: [
      {
        test: /\.js$/,
+       enforce: "pre",
        loader: "eslint-loader"
      }
    ]
  }
```


## `UglifyJsPlugin` sourceMap

The `sourceMap` option of the `UglifyJsPlugin` now defaults to `false` instead of `true`. This means that if you are using source maps for minimized code or want correct line numbers for uglifyjs warnings, you need to set `sourceMap: true` for `UglifyJsPlugin`.

``` diff
  devtool: "source-map",
  plugins: [
    new UglifyJsPlugin({
+     sourceMap: true
    })
  ]
```


## `UglifyJsPlugin` warnings

The `compress.warnings` option of the `UglifyJsPlugin` now defaults to `false` instead of `true`.
This means that if you want to see uglifyjs warnings, you need to set `compress.warnings` to `true`.

``` diff
  devtool: "source-map",
  plugins: [
    new UglifyJsPlugin({
+     compress: {
+       warnings: true
+     }
    })
  ]
```


## `UglifyJsPlugin` minimize loaders

`UglifyJsPlugin` no longer switches loaders into minimize mode. The `minimize: true` setting needs to be passed via loader options in the long-term. See loader documentation for relevant options.

The minimize mode for loaders will be removed in webpack 3 or later.

To keep compatibility with old loaders, loaders can be switched to minimize mode via plugin:

``` diff
  plugins: [
+   new webpack.LoaderOptionsPlugin({
+     minimize: true
+   })
  ]
```


## `DedupePlugin` has been removed

`webpack.optimize.DedupePlugin` isn't needed anymore. Remove it from your configuration.


## `BannerPlugin` - breaking change

`BannerPlugin` no longer accepts two parameters, but a single options object.

``` diff
  plugins: [
-    new webpack.BannerPlugin('Banner', {raw: true, entryOnly: true});
+    new webpack.BannerPlugin({banner: 'Banner', raw: true, entryOnly: true});
  ]
```


## `OccurrenceOrderPlugin` is now on by default

The `OccurrenceOrderPlugin` is now enabled by default and has been renamed (`OccurenceOrderPlugin` in webpack 1).
Thus make sure to remove the plugin from your configuration:

``` diff
  plugins: [
    // webpack 1
-   new webpack.optimize.OccurenceOrderPlugin()
    // webpack 2
-   new webpack.optimize.OccurrenceOrderPlugin()
  ]
```


## `ExtractTextWebpackPlugin` - breaking change

[ExtractTextPlugin](https://github.com/webpack/extract-text-webpack-plugin) requires version 2 to work with webpack 2.

`npm install --save-dev extract-text-webpack-plugin`

The configuration changes for this plugin are mainly syntactical.

### `ExtractTextPlugin.extract`

```diff
module: {
  rules: [
    {
      test: /.css$/,
-      loader: ExtractTextPlugin.extract("style-loader", "css-loader", { publicPath: "/dist" })
+      use: ExtractTextPlugin.extract({
+        fallback: "style-loader",
+        use: "css-loader",
+        publicPath: "/dist"
+      })
    }
  ]
}
```


### `new ExtractTextPlugin({options})`

```diff
plugins: [
-  new ExtractTextPlugin("bundle.css", { allChunks: true, disable: false })
+  new ExtractTextPlugin({
+    filename: "bundle.css",
+    disable: false,
+    allChunks: true
+  })
]
```


## Full dynamic requires now fail by default

A dependency with only an expression (i. e. `require(expr)`) will now create an empty context instead of the context of the complete directory.

Code like this should be refactored as it won't work with ES2015 modules. If this is not possible you can use the `ContextReplacementPlugin` to hint the compiler towards the correct resolving.

?> Link to an article about dynamic dependencies.

### Using custom arguments in CLI and configuration

If you abused the CLI to pass custom arguments to the configuration like so:

`webpack --custom-stuff`

``` js
// webpack.config.js
var customStuff = process.argv.indexOf("--custom-stuff") >= 0;
/* ... */
module.exports = config;
```

You may notice that this is no longer allowed. The CLI is more strict now.

Instead there is an interface for passing arguments to the configuration. This should be used instead. Future tools may rely on this.

`webpack --env.customStuff`

``` js
module.exports = function(env) {
  var customStuff = env.customStuff;
  /* ... */
  return config;
};
```

See [CLI](/api/cli).


## `require.ensure` and AMD `require` are asynchronous

These functions are now always asynchronous instead of calling their callback synchronously if the chunk is already loaded.

**`require.ensure` now depends upon native `Promise`s. If using `require.ensure` in an environment that lacks them then you will need a polyfill. **


## Loader configuration is through `options`

You can *no longer* configure a loader with a custom property in the `webpack.config.js`. It must be done through the `options`. The following configuration with the `ts` property is no longer valid with webpack 2:

```js
module.exports = {
  ...
  module: {
    rules: [{
      test: /\.tsx?$/,
      loader: 'ts-loader'
    }]
  },
  // does not work with webpack 2
  ts: { transpileOnly: false }
}
```


### What are `options`?

Good question. Well, strictly speaking it's 2 possible things; both ways to configure a webpack loader. Classically `options` was called `query` and was a string which could be appended to the name of the loader. Much like a query string but actually with [greater powers](https://github.com/webpack/loader-utils#parsequery):

```js
module.exports = {
  ...
  module: {
    rules: [{
      test: /\.tsx?$/,
      loader: 'ts-loader?' + JSON.stringify({ transpileOnly: false })
    }]
  }
}
```

But it can also be a separately specified object that's supplied alongside a loader:

```js
module.exports = {
  ...
  module: {
    rules: [{
      test: /\.tsx?$/,
      loader: 'ts-loader',
      options:  { transpileOnly: false }
    }]
  }
}
```


## `LoaderOptionsPlugin` context

Some loaders need context information and read them from the configuration. This needs to be passed via loader options in the long-term. See loader documentation for relevant options.

To keep compatibility with old loaders, this information can be passed via plugin:

``` diff
  plugins: [
+   new webpack.LoaderOptionsPlugin({
+     options: {
+       context: __dirname
+     }
+   })
  ]
```


## `debug`

The `debug` option switched loaders to debug mode in webpack 1. This needs to be passed via loader options in long-term. See loader documentation for relevant options.

The debug mode for loaders will be removed in webpack 3 or later.

To keep compatibility with old loaders, loaders can be switched to debug mode via a plugin:

``` diff
- debug: true,
  plugins: [
+   new webpack.LoaderOptionsPlugin({
+     debug: true
+   })
  ]
```


## Code Splitting with ES2015

In webpack 1, you could use [`require.ensure()`](/api/module-methods#require-ensure) as a method to lazily-load chunks for your application:

```javascript
require.ensure([], function(require) {
  var foo = require("./module");
});
```

The ES2015 Loader spec defines [`import()`](/api/module-methods#import-) as method to load ES2015 Modules dynamically on runtime. webpack treats `import()` as a split-point and puts the requested module in a separate chunk. `import()` takes the module name as argument and returns a Promise.

``` js
function onClick() {
  import("./module").then(module => {
    return module.default;
  }).catch(err => {
    console.log("Chunk loading failed");
  });
}
```

Good news: Failure to load a chunk can now be handled because they are `Promise` based.


## Dynamic expressions

It's possible to pass a partial expression to `import()`. This is handled similar to expressions in CommonJS (webpack creates a [context](https://webpack.github.io/docs/context.html) with all possible files).

`import()` creates a separate chunk for each possible module.

``` js
function route(path, query) {
  return import(`./routes/${path}/route`)
    .then(route => new route.Route(query));
}
// This creates a separate chunk for each possible route
```


## Mixing ES2015 with AMD and CommonJS

As for AMD and CommonJS you can freely mix all three module types (even within the same file). webpack behaves similar to babel and node-eps in this case:

```javascript
// CommonJS consuming ES2015 Module
var book = require("./book");

book.currentPage;
book.readPage();
book.default === "This is a book";
```

```javascript
// ES2015 Module consuming CommonJS
import fs from "fs"; // module.exports map to default
import { readFileSync } from "fs"; // named exports are read from returned object+

typeof fs.readFileSync === "function";
typeof readFileSync === "function";
```

It is important to note that you will want to tell Babel to not parse these module symbols so webpack can use them. You can do this by setting the following in your `.babelrc` or `babel-loader` options.

**.babelrc**

```json
{
  "presets": [
    ["es2015", { "modules": false }]
  ]
}
```


## Hints

No need to change something, but opportunities

### Template strings

webpack now supports template strings in expressions. This means you can start using them in webpack constructs:

``` diff
- require("./templates/" + name);
+ require(`./templates/${name}`);
```


### Configuration Promise

webpack now supports returning a `Promise` from the configuration file. This allows to do async processing in you configuration file.

**webpack.config.js**

``` js
module.exports = function() {
  return fetchLangs().then(lang => ({
    entry: "...",
    // ...
    plugins: [
      new DefinePlugin({ LANGUAGE: lang })
    ]
  }));
};
```


### Advanced loader matching

webpack now supports more things to match on for loaders.

``` js
module: {
  rules: [
    {
      resource: /filename/, // matches "/path/filename.js"
      resourceQuery: /^\?querystring$/, // matches "?querystring"
      issuer: /filename/, // matches "/path/something.js" if requested from "/path/filename.js"
    }
  ]
}
```


### More CLI options

There are some new CLI options for you to use:

`--define process.env.NODE_ENV="production"` See [`DefinePlugin`](/plugins/define-plugin/).

`--display-depth` displays the distance to the entry point for each module.

`--display-used-exports` display info about which exports are used in a module.

`--display-max-modules` sets the number for modules displayed in the output (defaults to 15).

`-p` also defines `process.env.NODE_ENV` to `"production"` now.


## Loader changes

Changes only relevant for loader authors.


### Cacheable

Loaders are now cacheable by default. Loaders must opt-out if they are not cacheable.

``` diff
  // Cacheable loader
  module.exports = function(source) {
-   this.cacheable();
    return source;
  }
```

``` diff
  // Not cacheable loader
  module.exports = function(source) {
+   this.cacheable(false);
    return source;
  }
```


### Complex options

__webpack 1__ only supports `JSON.stringify`-able options for loaders.

__webpack 2__ now supports any JS object as loader options.

Before webpack [2.2.1](https://github.com/webpack/webpack/releases/tag/v2.2.1) (i.e. from 2.0.0 through 2.2.0), using complex options required using `ident` for the `options` object to allow its reference from other loaders. __This was removed in 2.2.1__ and thus current migrations do not require any use of the `ident` key.

```diff
{
  test: /\.ext/
  use: {
    loader: '...',
    options: {
-     ident: 'id',
      fn: () => require('./foo.js')
    }
  }
}
```
