import env from 'react-native-config';
import axios from "axios";
import { Linking } from 'react-native';
import { NetworkInfo } from 'react-native-network-info';
import { canOpenUrl } from '../helpers/LinkHelper';
import StorageService from './StorageService';

const TOKENKEY = 'accessToken';

let cancelled = false;

/**
 * Reset cancel flag
 */
export const resetCancel = () => {
  cancelled = false;
}

/**
 * Launch BankID app
 * @param {string} bankIdClientUrl
 */
launchBankIdApp = async (autoStartToken) => {
  const bankIdClientUrl = this.buildBankIdClientUrl(autoStartToken);

  return this.openURL(bankIdClientUrl);
};

/**
 * Builds the BankID client URL
 * @param {string} autoStartToken
 */
buildBankIdClientUrl = (autoStartToken) => {
  const params = `?autostarttoken=${autoStartToken}&redirect=${env.APP_SCHEME}://`;
  const androidUrl = 'bankid:///';
  const iosUrl = 'https://app.bankid.com/';

  return `${iosUrl}${params}`;
};

/**
 * Open requested URL
 * @param {string} url
 */
openURL = (url) => {
  return Linking.openURL(url)
    .then(() => true)
    .catch(() => false);
};

/**
 * Make an auth request to BankID API and poll until done
 * @param {string} personalNumber
 */
export const authorize = (personalNumber) =>
  new Promise(async (resolve, reject) => {
    const endUserIp = await NetworkInfo.getIPAddress(ip => ip);
    let responseJson;

    // Make initial auth request to retrieve user details and access token
    try {
      responseJson = await request(
        'auth/bankid',
        { personalNumber, endUserIp }
      );
      // data = auth.data.attributes;
      // token = auth.data.attributes.token;
    } catch (error) {
      console.log("Auth error", error);
      return reject(error);
    }

    const autoStartToken = responseJson.data.attributes.auto_start_token;
    const orderRef = responseJson.data.attributes.order_ref;
    const token = responseJson.data.attributes.token;

    if (!autoStartToken || !orderRef) {
      return reject(new Error('Missing autoStartToken or orderRef'));
    }

    // Save order reference + temporary access token to async storage
    StorageService.saveData('orderRef', orderRef);
    StorageService.saveData('tempAccessToken', token);

    // Launch BankID app if it's installed on this machine
    const launchNativeApp = await canOpenUrl('bankid:///');
    if (launchNativeApp) {
      this.launchBankIdApp(autoStartToken);
    }

    // Poll /collect/ endpoint every 2nd second until auth either success or fails
    const interval = setInterval(async () => {
      // Bail if cancel button is triggered by the user
      if (cancelled === true) {
        clearInterval(interval);
        resetCancel();
        return resolve({ ok: false, data: "cancelled" });
      }

      let collectData = {};

      try {
        const response = await request(
          `auth/bankid/collect`,
          { orderRef },
          token
        );

        collectData = response.data.attributes;

      } catch (error) {
        clearInterval(interval);
        reject(error);
      }

      const { status, hint_code, completion_data } = collectData;

      console.log("status", status);
      console.log("hint_code", hint_code);
      console.log("completion_data", completion_data);

      if (status === 'failed') {
        clearInterval(interval);
        resolve({ ok: false, data: hint_code });
      } else if (status === 'complete') {
        clearInterval(interval);

        if (completion_data.user) {
          resolve({
            ok: true,
            data: {
              user: completion_data.user,
              accessToken: token
            }
          });
        }

        resolve({ ok: false, data: hint_code });
      }
    }, 2000);
  });

/**
* Make a sign request to BankID API and poll until done
* @param {string} personalNumber
*/
export const sign = (personalNumber, userVisibleData) =>
  new Promise(async (resolve, reject) => {
    const endUserIp = await NetworkInfo.getIPAddress(ip => ip);
    const token = await StorageService.getData(TOKENKEY);
    let user = {};

    // Make initial auth request to retrieve user details and access token
    try {
      const signResponse = await request(
        'auth/sign',
        {
          personalNumber,
          endUserIp,
          userVisibleData,
        },
        token
      );
      user = signResponse.user;
    } catch (error) {
      console.log("Sign error", error.message);
      return reject(error);
    }

    const { autoStartToken, orderRef } = user;

    if (!autoStartToken || !orderRef) {
      return reject(new Error('Missing autoStartToken or orderRef'));
    }

    // Save order reference to async storage
    StorageService.saveData('orderRef', orderRef);

    // Launch BankID app if it's installed on this machine
    const launchNativeApp = await canOpenUrl('bankid:///');
    if (launchNativeApp) {
      this.launchBankIdApp(autoStartToken);
    }

    // Poll /collect/ endpoint every 2nd second until auth either success or fails
    const interval = setInterval(async () => {
      // Bail if cancel button is triggered by the user
      if (cancelled === true) {
        clearInterval(interval);
        resetCancel();
        return resolve({ ok: false, data: "cancelled" });
      }

      let collectData = {};

      try {
        const response = await request(
          `auth/${orderRef}`,
          {},
          token
        );

        collectData = response.data;

      } catch (error) {
        clearInterval(interval);
        reject(error);
      }

      const { status, hintCode, completionData } = collectData;

      if (status === 'failed') {
        clearInterval(interval);
        resolve({ ok: false, data: hintCode });
      } else if (status === 'complete') {
        clearInterval(interval);

        if (completionData.user) {
          resolve({
            ok: true,
            data: {
              user: completionData.user,
              accessToken: token
            }
          });
        }

        resolve({ ok: false, data: hintCode });
      }
    }, 2000);
  });

/**
 * Cancels a started BankID request
 * @param {string} order
 */
export const cancelRequest = async () => {
  const orderRef = await StorageService.getData('orderRef');
  const token = await StorageService.getData('tempAccessToken');

  console.log("Cancel order", orderRef);
  console.log("Cancel order with temporary accessToken", token);

  // Stop polling auth/sign requests
  cancelled = true;

  // Send cancel request
  try {
    await request(
      `auth/cancel/${orderRef}`,
      {},
      token
    );
  } catch (err) {
    console.log("Cancel err", err)
  }
}

/**
 * Send request to BankID API
 * @param {string} endpoint
 * @param {array} params
 */
request = async (endpoint, data, token) => {
  return new Promise(async (resolve, reject) => {
    await axios({
      method: 'POST',
      url: `${env.MITTHELSINGBORG_IO}/${endpoint}`,
      data: data,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
      }
    }
    ).then(result => {
      console.log("Request result", result);
      return resolve(result.data);
    }).catch(err => {
      console.log("Error in request call", err.request);
      return reject(err);
    });
  });
}

/**
 * Bypasses the BankID authentication steps
 * @param {string} personalNumber
 */
export const bypassBankid = async (personalNumber) => {
  return {
    ok: true,
    data: {
      user: {
        'name': 'Saruman Stål',
        'givenName': 'Saruman',
        'surname': 'Stål',
        'personalNumber': personalNumber
      },
    }
  }
};
