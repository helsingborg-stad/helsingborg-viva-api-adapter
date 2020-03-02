module.exports = {
  presets: ['module:metro-react-native-babel-preset'],
  plugins: [
    /**
     * Resolve custom alias paths in Babel
     */
    [
      require.resolve('babel-plugin-module-resolver'),
      {
        root: ['./'],
        alias: {
          app: './source',
          storybook: './storybook',
        },
      },
    ],
  ],
};
