var path = require("path");
console.log(path.join(__dirname));

const webpack = require("webpack");
const autoprefixer = require("autoprefixer");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CopyWebpackPlugin = require("copy-webpack-plugin");

module.exports = {
    entry: ["./scss/main.scss", "./js/main.js"],
    output: {
        path: path.resolve(__dirname, "dist"),
        filename: "bundle.js",
        publicPath: "/",
    },

    module: {
        rules: [
            {
                test: /\.scss$/,
                use: [
                    { loader: MiniCssExtractPlugin.loader },
                    { loader: "css-loader" },
                    {
                        loader: "postcss-loader",
                        options: {
                            postcssOptions: {
                                plugins: [autoprefixer()],
                            },
                        },
                    },
                    {
                        loader: "sass-loader",
                        options: {
                            sassOptions: {
                                includePaths: ["./node_modules"],
                            },
                            implementation: require("sass"),
                            webpackImporter: false, // See https://github.com/webpack-contrib/sass-loader/issues/804
                        },
                    },
                ],
            },
        ],
    },

    plugins: [
        // new CopyWebpackPlugin({
        //     patterns: [
        //         { from: "./template/index.html", to: "./index.html" },
        //     ],
        // }),

        new MiniCssExtractPlugin({
            // filename: "[name].css",
            // chunkFilename: "[id].css",
            filename: "bundle.css",
        }),

        new webpack.ProvidePlugin({
            $: "jquery",
            jQuery: "jquery",
        }),
    ],
};
