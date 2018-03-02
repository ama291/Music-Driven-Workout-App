
//  CEFilterViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Christopher Choy on 2/25/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//
import UIKit

class CEFilterViewController: UIViewController, UIPickerViewDelegate, UIPickerViewDataSource {
    
    @IBOutlet weak var catPicker: UIPickerView!
    @IBOutlet weak var musclePicker: UIPickerView!
    @IBOutlet weak var equipPicker: UIPickerView!

    
    var category: String = ""
    var muscleGroup: String = ""
    var equipment: String = ""
    var userid: String! = "1"
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if segue.destination is CESelectionViewController
        {
            let vc = segue.destination as? CESelectionViewController
            //data to send
            vc?.category = category
            vc?.muscleGroup = muscleGroup
            vc?.equipment = equipment
            vc?.userid = userid
        }
    }
    
    
    
    var catList: [String] = [String]()
    var muscleList: [String] = [String]()
    var equipList: [String] = [String]()
    
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        print("user: \(userid)")
        
        //json response struct - need to change this to what you expect the result to be
        struct Post: Codable {
            let key: String
        }
        self.catPicker.delegate = self
        self.catPicker.dataSource = self
        catList = ["Any", "Strength", "Stretching", "Olympic Weightlifting", "Strongman", "Plyometrics", "Cardio", "Powerlifting"]
        
        self.musclePicker.delegate = self
        self.musclePicker.dataSource = self
        muscleList = ["Any", "Neck", "Traps", "Shoulders", "Chest", "Biceps", "Forearms", "Abdominals", "Quadriceps", "Calves", "Triceps", "Lats", "Middle Back", "Lower Back", "Glutes", "Hamstrings"]
        
        self.equipPicker.delegate = self
        self.equipPicker.dataSource = self
        equipList = ["Body Only", "Any", "Other", "None", "Machine", "Dumbbell", "Kettlebells", "Barbell", "Cable", "Bands", "Medicine Ball", "E-Z Curl Bar", "Exercise Ball", "Foam Roll"]
        
        
        // Do any additional setup after loading the view.
    }
    
    func numberOfComponents(in pickerView: UIPickerView) -> Int {
        return 1
    }
    
    func pickerView(_ pickerView: UIPickerView, numberOfRowsInComponent component: Int) -> Int {
        if pickerView == catPicker {
            return catList.count
        }
        else if pickerView == musclePicker {
            return muscleList.count
        }
        else if pickerView == equipPicker {
            return equipList.count
        }
        return 0
    }
    
    func pickerView(_ pickerView: UIPickerView, titleForRow row: Int, forComponent component: Int) -> String? {
        if pickerView == catPicker {
            return catList[row]
        }
        else if pickerView == musclePicker {
            return muscleList[row]
        }
        else if pickerView == equipPicker {
            return equipList[row]
        }
        return ""
    }
    
    
    @IBAction func getExercises(_ sender: Any) {
        category = catList[catPicker.selectedRow(inComponent: 0)]
        muscleGroup = muscleList[musclePicker.selectedRow(inComponent: 0)]
        equipment = equipList[equipPicker.selectedRow(inComponent: 0)]
        
        print(category, muscleGroup, equipment)
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
    
    @IBAction func goToHome(_ sender: Any) {
        let storyboard = UIStoryboard(name: "Main", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "homeID") as! MenuViewController
        vc.userid = userid!
        present(vc, animated: true, completion: nil)
    }
    
}



