//
//  WorkSelectionViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Christopher Choy on 2/25/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit

class WorkSelectionViewController: UIViewController, UIPickerViewDelegate, UIPickerViewDataSource {

    // fields to pass to WorkSummaryVC
    var themes = ""
    var categories = ""
    var musclegroup = ""
    var equipment = ""
    var duration = ""
    var difficulty = ""
    var theme: [String:Any]!
    var themeIndex: Int!
    var allThemes: [[String:Any]] = []
    var themeSpotifyID: String!
    //var player: SPTAudioStreamingController?

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        
        self.durationPicker.delegate = self
        self.durationPicker.dataSource = self
        self.themesPicker.delegate = self
        self.themesPicker.dataSource = self

        global.token = "b82cb70f-0f2e-4591-a892-a0b5bef45b9a" //TODO: populate this example token
        hideCategories()
        populateThemesPicker()
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


    /* Navigation */
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if segue.destination is WorkSummaryViewController {
            let vc = segue.destination as? WorkSummaryViewController
            //data to send
            vc?.categories = categories
            vc?.musclegroup = musclegroup
            vc?.equipment = equipment
            vc?.duration = duration
            vc?.difficulty = difficulty
            vc?.themes = themes
            vc?.themeSpotifyId = self.themeSpotifyID!
            //vc?.player = player!
        }
    }
    override func shouldPerformSegue(withIdentifier identifier: String, sender: Any?) -> Bool {
        if (categories.isEmpty && musclegroup.isEmpty) {
            let alert = UIAlertController(title: "Error", message: "You must select at least one Category or Muscle Group", preferredStyle: UIAlertControllerStyle.alert)
            alert.addAction(UIAlertAction(title: "kk.", style: UIAlertActionStyle.default, handler: nil))
            self.present(alert, animated: true, completion: nil)
            return false
        }
        return true
    }
    
    @IBAction func goToHome(_ sender: UIButton) {
        let storyboard = UIStoryboard(name: "Main", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "homeID") as! MenuViewController
        present(vc, animated: true, completion: nil)
    }

    /* Category switches & labels */
    @IBOutlet weak var categoryswitch: UISwitch!

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

    //equipment switches and labels
    @IBOutlet weak var bodyswitch: UISwitch!
    @IBOutlet weak var machineswitch: UISwitch!
    @IBOutlet weak var dumbswitch: UISwitch!
    @IBOutlet weak var kettleswitch: UISwitch!
    @IBOutlet weak var barswitch: UISwitch!
    @IBOutlet weak var cableswitch: UISwitch!
    @IBOutlet weak var bandswitch: UISwitch!
    @IBOutlet weak var medswitch: UISwitch!
    @IBOutlet weak var ezswitch: UISwitch!
    @IBOutlet weak var eballswitch: UISwitch!
    @IBOutlet weak var foamswitch: UISwitch!
    @IBOutlet weak var otherswitch: UISwitch!
    @IBOutlet weak var noneswitch: UISwitch!


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
        if (categoryswitch.isOn) {
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

    /* Duraton Picker Stuff */
    @IBOutlet weak var durationPicker: UIPickerView!
    let durationOptions = ["10","15","20","25","30","35","40","45","50","55","60"]

    // number of columns of data
    func numberOfComponents(in pickerView: UIPickerView) -> Int {
        return 1
    }
    // number of rows in data
    func pickerView(_ pickerView: UIPickerView, numberOfRowsInComponent component: Int) -> Int {
        if pickerView == durationPicker {
            return durationOptions.count
        } else if pickerView == themesPicker {
            return themesOptions.count
        }
        return 0
    }
    // data to return for row and column
    func pickerView(_ pickerView: UIPickerView, titleForRow row: Int, forComponent component: Int) -> String? {
        if pickerView == durationPicker {
            return durationOptions[row]
        } else if pickerView == themesPicker {
            // print("THEMES PICKER")
            // print(row)
            // print(themesOptions[row])
            if row == 0 {
                self.themeSpotifyID = "Any"
            }
            else {
                // print(self.allThemes[row-1])
                self.themeSpotifyID = self.allThemes[row-1]["spotifyId"] as! String
                // print(self.themeSpotifyID)
            }
            return themesOptions[row]
        }
        return ""
    }
    // Catpure the pickerview selection
    func pickerView(_ pickerView: UIPickerView, didSelectRow row: Int, inComponent component: Int) {
        // This method is triggered whenever the user makes a change to the picker selection.
        // The parameter named row and component represents what was selected.
        if pickerView == durationPicker {
            duration = durationOptions[row]
        } else {
            self.themeIndex = row
            
        }
    }

    /* Themes Stuff */
    @IBOutlet weak var themesPicker: UIPickerView!
    var themesOptions: [String] = ["Any"]
    
    func populateThemesPicker() {
        /* Make the API Call */
        let request = APIRequest()
        
        let qstr = "userid=\(global.userid!)&key=SoftCon2018"
        request.submitPostServer(route: "/api/workouts/themessaved/", qstring: qstr) { (data, response, error) -> Void in
            if let error = error {
                fatalError(error.localizedDescription)
            }
            let resultjson = try? JSONSerialization.jsonObject(with: data!, options: [])

            if let arr = resultjson as? [Dictionary<String,Any>] {
                for obj in arr {
                    // Populate themesOptions
                    self.themesOptions.append(obj["name"] as! String)
                    self.allThemes.append(obj)
                }
            }
            
            /* Reload the Picker */
            DispatchQueue.main.async {
                self.themesPicker.reloadAllComponents()
            }
           
        }.resume()
        
    }

    @IBOutlet weak var difficultyswitch: UISwitch!

    /* getWorkoutAction - sets variables to send to next screen */
    @IBOutlet weak var getworkout: UIButton!
    @IBAction func getWorkoutAction(_ sender: Any) {
        /* CATEGRY or MUSCLEGROUP */
        if (categoryswitch.isOn) {
            if (neckswitch.isOn) {
                musclegroup += "Neck,"
            }
            if (trapsswitch.isOn) {
                musclegroup += "Traps,"
            }
            if (shouldersswitch.isOn) {
                musclegroup += "Shoulders,"
            }
            if (chestswitch.isOn) {
                musclegroup += "Chest,"
            }
            if (bicepsswitch.isOn) {
                musclegroup += "Biceps,"
            }
            if (forearmsswitch.isOn) {
                musclegroup += "Forearms,"
            }
            if (abdominalsswitch.isOn) {
                musclegroup += "Abdominals,"
            }
            if (quadricepsswitch.isOn) {
                musclegroup += "Quadriceps,"
            }
            if (calvesswitch.isOn) {
                musclegroup += "Calves,"
            }
            if (tricepsswitch.isOn) {
                musclegroup += "Triceps,"
            }
            if (latsswitch.isOn) {
                musclegroup += "Lats,"
            }
            if (middlebackswitch.isOn) {
                musclegroup += "Middle Back,"
            }
            if (lowerbackswitch.isOn) {
                musclegroup += "Lower Back,"
            }
            if (glutesswitch.isOn) {
                musclegroup += "Glutes,"
            }
            if (hamstringsswitch.isOn) {
                musclegroup += "Hamstrings,"
            }
        }

        else {
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

        }
        
        if (categories.last == ",") {
            categories.removeLast()
        }
        if (musclegroup.last == ",") {
            musclegroup.removeLast()
        }
        
        /* EQUIPMENT */
        equipment = ""
        if (bodyswitch.isOn) {
            equipment += "Body Only,"
        }
        if (machineswitch.isOn) {
            equipment += "Machine,"
        }
        if (dumbswitch.isOn) {
            equipment += "Dumbbell,"
        }
        if (kettleswitch.isOn) {
            equipment += "Kettlebells,"
        }
        if (barswitch.isOn) {
            equipment += "Barbell,"
        }
        if (cableswitch.isOn) {
            equipment += "Cable,"
        }
        if (bandswitch.isOn) {
            equipment += "Bands,"
        }
        if (medswitch.isOn) {
            equipment += "Medicine Ball,"
        }
        if (ezswitch.isOn) {
            equipment += "E-Z Curl Bar,"
        }
        if (eballswitch.isOn) {
            equipment += "Exercise Ball,"
        }
        if (foamswitch.isOn) {
            equipment += "Foam roll,"
        }
        if (otherswitch.isOn) {
            equipment += "Other,"
        }
        if (noneswitch.isOn) {
            equipment += "None,"
        }
        if (equipment.last == ",") {
            equipment.removeLast()
        }
        if equipment.isEmpty {
            equipment = "None"
        }


        if duration.isEmpty {
            duration = "10"
        }

        if (difficultyswitch.isOn) {
            difficulty = "Intermediate"
        }
        else {
            difficulty = "Beginner"
        }
        
        /* ERROR CHECKS */
        if (categories.isEmpty && musclegroup.isEmpty) {
            let alert = UIAlertController(title: "Error", message: "You must select at least one Category or Muscle Group", preferredStyle: UIAlertControllerStyle.alert)
            alert.addAction(UIAlertAction(title: "kk.", style: UIAlertActionStyle.default, handler: nil))
            self.present(alert, animated: true, completion: nil)
            return
        }
            
        self.performSegue(withIdentifier: "summarySegue", sender: self)
    }
}
