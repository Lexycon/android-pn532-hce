package com.lexycon.hostcardemulation

import android.content.Intent
import android.nfc.NfcAdapter
import android.os.Bundle
import android.provider.Settings
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import kotlinx.android.synthetic.main.activity_main.*


class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val dataStore = DataStoreUtil(this)
        var uid = dataStore.getID()
        textID.setText(uid)


        buttonGenerate.setOnClickListener{
            uid = dataStore.generateID()
            dataStore.saveID(uid)
            textID.setText(uid)
        }


        val nfcAdapter = NfcAdapter.getDefaultAdapter(this)
        if (nfcAdapter != null) {
            if (!nfcAdapter.isEnabled) {
                Toast.makeText(this, R.string.nfc_deactivated, Toast.LENGTH_LONG).show()
            }
        } else{
            Toast.makeText(this, R.string.nfc_unsupported, Toast.LENGTH_LONG).show()
        }
    }

}
