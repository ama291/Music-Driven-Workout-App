//
//  WorkSelectionViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Christopher Choy on 2/25/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit

class WorkSelectionViewController: UIViewController {
    
    var userid: String!
    var themes = ""
    var categories = ""
    var musclegroup = ""
    var equipment = ""
    var duration = ""
    var difficulty = ""
    //TODO: populate this example token
    var token = "b82cb70f-0f2e-4591-a892-a0b5bef45b9a"
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        
        hideCategories()
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if segue.destination is WorkSummaryViewController {
            let vc = segue.destination as? WorkSummaryViewController
            //data to send
            vc?.userid = userid!
        }
    }
    @IBAction func goToHome(_ sender: UIButton) {
        let storyboard = UIStoryboard(name: "Main", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "homeID") as! MenuViewController
        vc.userid = userid!
        present(vc, animated: true, completion: nil)
    }
    
    @IBOutlet weak var categoryswitch: UISwitch!
    @IBOutlet weak var category: UITableView!
    
    //category switches & labels
    @IBOutlet weak var strengthswitch: UISwitch!
    @IBOutlet weak var stretchingswitch: UISwitch!
    @IBOutlet weak var weightliftingswitch: UISwitch!
    @IBOutlet weak var strongmanswitch: UISwitch!
    @IBOutlet weak var plyometricsswitch: UISwitch!
    @IBOutlet weak var cardioswitch: UISwitch!
    @IBOutlet weak var powerliftingswitch: UISwitch!
    @IBOutlet weak var strlabel: UILabel!
    @IBOutlet weak var stretchlabel: UILabel!
    @IBOutlet weak var weightlabel: UILabel!
    @IBOutlet weak var stronglabel: UILabel!
    @IBOutlet weak var plylabel: UILabel!
    @IBOutlet weak var cardiolabel: UILabel!
    @IBOutlet weak var powerlabel: UILabel!
    
    //muscle group switches & labels
    @IBOutlet weak var neckswitch: UISwitch!
    @IBOutlet weak var trapsswitch: UISwitch!
    @IBOutlet weak var shouldersswitch: UISwitch!
    @IBOutlet weak var chestswitch: UISwitch!
    @IBOutlet weak var bicepsswitch: UISwitch!
    @IBOutlet weak var forearmsswitch: UISwitch!
    @IBOutlet weak var abdominalsswitch: UISwitch!
    @IBOutlet weak var quadricepsswitch: UISwitch!
    @IBOutlet weak var calvesswitch: UISwitch!
    @IBOutlet weak var tricepsswitch: UISwitch!
    @IBOutlet weak var latsswitch: UISwitch!
    @IBOutlet weak var middlebackswitch: UISwitch!
    @IBOutlet weak var lowerbackswitch: UISwitch!
    @IBOutlet weak var glutesswitch: UISwitch!
    @IBOutlet weak var hamstringsswitch: UISwitch!
    @IBOutlet weak var necklabel: UILabel!
    @IBOutlet weak var traplabel: UILabel!
    @IBOutlet weak var shoulderlabel: UILabel!
    @IBOutlet weak var chestlabel: UILabel!
    @IBOutlet weak var biceplabel: UILabel!
    @IBOutlet weak var forearmlabel: UILabel!
    @IBOutlet weak var ablabel: UILabel!
    @IBOutlet weak var quadlabel: UILabel!
    @IBOutlet weak var calveslabel: UILabel!
    @IBOutlet weak var trilabel: UILabel!
    @IBOutlet weak var latlabel: UILabel!
    @IBOutlet weak var midlabel: UILabel!
    @IBOutlet weak var lowlabel: UILabel!
    @IBOutlet weak var glutelabel: UILabel!
    @IBOutlet weak var hamlabel: UILabel!
    
    @objc func hideCategories() {
        strengthswitch.isHidden = true
        stretchingswitch.isHidden = true
        weightliftingswitch.isHidden = true
        strongmanswitch.isHidden = true
        plyometricsswitch.isHidden = true
        cardioswitch.isHidden = true
        powerliftingswitch.isHidden = true
        strlabel.isHidden = true
        stretchlabel.isHidden = true
        weightlabel.isHidden = true
        stronglabel.isHidden = true
        plylabel.isHidden = true
        cardiolabel.isHidden = true
        powerlabel.isHidden = true
    }
    
    //TODO: need to deactivate category or muscle group on switch
    @IBAction func switchToggled(_ sender: Any) {
        let status = categoryswitch.isOn
        if (status) {
            strengthswitch.isHidden = true
            stretchingswitch.isHidden = true
            weightliftingswitch.isHidden = true
            strongmanswitch.isHidden = true
            plyometricsswitch.isHidden = true
            cardioswitch.isHidden = true
            powerliftingswitch.isHidden = true
            strlabel.isHidden = true
            stretchlabel.isHidden = true
            weightlabel.isHidden = true
            stronglabel.isHidden = true
            plylabel.isHidden = true
            cardiolabel.isHidden = true
            powerlabel.isHidden = true
            neckswitch.isHidden = false
            trapsswitch.isHidden = false
            shouldersswitch.isHidden = false
            chestswitch.isHidden = false
            bicepsswitch.isHidden = false
            forearmsswitch.isHidden = false
            abdominalsswitch.isHidden = false
            quadricepsswitch.isHidden = false
            calvesswitch.isHidden = false
            tricepsswitch.isHidden = false
            latsswitch.isHidden = false
            middlebackswitch.isHidden = false
            lowerbackswitch.isHidden = false
            glutesswitch.isHidden = false
            hamstringsswitch.isHidden = false
            necklabel.isHidden = false
            traplabel.isHidden = false
            shoulderlabel.isHidden = false
            chestlabel.isHidden = false
            biceplabel.isHidden = false
            forearmlabel.isHidden = false
            ablabel.isHidden = false
            quadlabel.isHidden = false
            calveslabel.isHidden = false
            trilabel.isHidden = false
            latlabel.isHidden = false
            midlabel.isHidden = false
            lowlabel.isHidden = false
            glutelabel.isHidden = false
            hamlabel.isHidden = false
        }
        else {
            neckswitch.isHidden = true
            trapsswitch.isHidden = true
            shouldersswitch.isHidden = true
            chestswitch.isHidden = true
            bicepsswitch.isHidden = true
            forearmsswitch.isHidden = true
            abdominalsswitch.isHidden = true
            quadricepsswitch.isHidden = true
            calvesswitch.isHidden = true
            tricepsswitch.isHidden = true
            latsswitch.isHidden = true
            middlebackswitch.isHidden = true
            lowerbackswitch.isHidden = true
            glutesswitch.isHidden = true
            hamstringsswitch.isHidden = true
            necklabel.isHidden = true
            traplabel.isHidden = true
            shoulderlabel.isHidden = true
            chestlabel.isHidden = true
            biceplabel.isHidden = true
            forearmlabel.isHidden = true
            ablabel.isHidden = true
            quadlabel.isHidden = true
            calveslabel.isHidden = true
            trilabel.isHidden = true
            latlabel.isHidden = true
            midlabel.isHidden = true
            lowlabel.isHidden = true
            glutelabel.isHidden = true
            hamlabel.isHidden = true
            strengthswitch.isHidden = false
            stretchingswitch.isHidden = false
            weightliftingswitch.isHidden = false
            strongmanswitch.isHidden = false
            plyometricsswitch.isHidden = false
            cardioswitch.isHidden = false
            powerliftingswitch.isHidden = false
            strlabel.isHidden = false
            stretchlabel.isHidden = false
            weightlabel.isHidden = false
            stronglabel.isHidden = false
            plylabel.isHidden = false
            cardiolabel.isHidden = false
            powerlabel.isHidden = false
            
        }
    }
    
    //equipment switches
    @IBOutlet weak var bodyonly: UISwitch!
    @IBOutlet weak var machine: UISwitch!
    @IBOutlet weak var Dumbbell: UISwitch!
    @IBOutlet weak var Kettlebells: UISwitch!
    @IBOutlet weak var barbell: UISwitch!
    @IBOutlet weak var cable: UISwitch!
    @IBOutlet weak var bands: UISwitch!
    @IBOutlet weak var medicineball: UISwitch!
    @IBOutlet weak var ezcurl: UISwitch!
    @IBOutlet weak var exerciseball: UISwitch!
    @IBOutlet weak var foamroll: UISwitch!
    @IBOutlet weak var other: UISwitch!
    @IBOutlet weak var none: UISwitch!
    
    @IBOutlet weak var dur: UITextField!
    
    //TODO: check input, themes
    @IBOutlet weak var getworkout: UIButton!
    @IBAction func getWorkoutAction(_ sender: Any) {
        if (strengthswitch.isOn) {
            categories += "Strength,"
        }
        if (stretchingswitch.isOn) {
            categories += "Stretching,"
        }
        if (weightliftingswitch.isOn) {
            categories += "Olympic Weightlifting,"
        }
        if (strongmanswitch.isOn) {
            categories += "Strongman,"
        }
        if (plyometricsswitch.isOn) {
            categories += "Plyometrics,"
        }
        if (cardioswitch.isOn) {
            categories += "Cardio,"
        }
        if (powerliftingswitch.isOn) {
            categories += "Powerlifting,"
        }
        if (categories.last == ",") {
            categories.removeLast()
        }
        print(categories)
    }
}
