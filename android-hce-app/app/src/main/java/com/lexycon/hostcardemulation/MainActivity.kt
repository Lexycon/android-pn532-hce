package com.lexycon.hostcardemulation

import android.nfc.NfcAdapter
import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import kotlinx.android.synthetic.main.activity_main.*


class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val dataStore = DataStoreUtil(this)
        val uid = dataStore.getID()
        textID.text = uid

        val nfcAdapter = NfcAdapter.getDefaultAdapter(this)
        if (nfcAdapter != null) {
            if (!nfcAdapter.isEnabled) {
                NFCDialog(this).showNFCDisabled()
            }
        } else{
            NFCDialog(this).showNFCUnsupported()
        }




    }

}
