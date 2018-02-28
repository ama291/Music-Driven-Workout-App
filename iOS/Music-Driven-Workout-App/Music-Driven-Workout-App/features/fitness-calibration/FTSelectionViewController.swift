//
//  FTSelectionViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Christopher Choy on 2/25/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit

class FTSelectionViewController: UIViewController, UIPickerViewDelegate, UIPickerViewDataSource {
    @IBOutlet weak var catPicker: UIPickerView!
    @IBOutlet weak var numLabel: UILabel!
    
    var category: String = ""
    var numEx: Int = 1
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if segue.destination is FTChooseTracked
        {
            let vc = segue.destination as? FTChooseTracked
            //data to send
            vc?.category = category
            vc?.numEx = numEx
        }
    }
    
    var userid: String!
    var catList: [String] = [String]()
    

    override func viewDidLoad() {
        super.viewDidLoad()
        
        self.catPicker.delegate = self
        self.catPicker.dataSource = self
        catList = ["Strength", "Stretching", "Olympic Weightlifting", "Strongman", "Plyometrics", "Cardio", "Powerlifting"]
        
        // Do any additional setup after loading the view.
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    func numberOfComponents(in pickerView: UIPickerView) -> Int {
        return 1
    }
    
    func pickerView(_ pickerView: UIPickerView, numberOfRowsInComponent component: Int) -> Int {
        if pickerView == catPicker {
            return catList.count
        }
        return 0
    }
    
    func pickerView(_ pickerView: UIPickerView, titleForRow row: Int, forComponent component: Int) -> String? {
        if pickerView == catPicker {
            return catList[row]
        }
        return ""
    }
    

    @IBAction func numChanged(_ sender: UISlider) {
        numEx = Int(sender.value)
        numLabel.text = "Number of Exercises: " + String(numEx)
    }
    
    @IBAction func createTest(_ sender: Any) {
        category = catList[catPicker.selectedRow(inComponent: 0)]
    }
    
    /*
     // MARK: - Navigation
     
     // In a storyboard-based application, you will often want to do a little preparation before navigation
     override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
     // Get the new view controller using segue.destinationViewController.
     // Pass the selected object to the new view controller.
     }
     */
    @IBAction func goToHome(_ sender: UIButton) {
        let storyboard = UIStoryboard(name: "Main", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "homeID") as! MenuViewController
        vc.userid = userid!
        present(vc, animated: true, completion: nil)
    }
    
}

