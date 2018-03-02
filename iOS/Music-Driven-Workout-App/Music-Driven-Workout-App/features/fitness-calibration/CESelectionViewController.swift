//
//  CESelectionViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Christopher Choy on 2/25/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//
import UIKit

class CESelectionViewController: UIViewController, UIPickerViewDelegate, UIPickerViewDataSource {
    
    @IBOutlet weak var exPicker: UIPickerView!
    
    var category: String = ""
    var muscleGroup: String = ""
    var equipment: String = ""
    var userid: String!
    
    var reply: [[String:Any]] = [[String:Any]]()
    var exerciseInfo: [String:Any] = [String:Any]()
    var isCalibration: Bool = true
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if segue.destination is FTExDescViewController
        {
            let vc = segue.destination as? FTExDescViewController
            //data to send
            vc?.exerciseInfo = exerciseInfo
            vc?.isCalibration = isCalibration
            vc?.userid = userid
        }
    }
    
    var exList: [String] = [String]()
    override func viewDidLoad() {
        super.viewDidLoad()
        print("user: \(userid)")

        let request = APIRequest()
        
        print("New view:", category, muscleGroup, equipment)
        let qstr = "category=" + category + "&muscle=" + muscleGroup + "&equipment=" + equipment + "&key=SoftCon2018"
        
        request.submitPostLocal(route: "/api/fitness/getexsbytype/", qstring: qstr) { (data, response, error) -> Void in
            if let error = error {
                fatalError(error.localizedDescription)
            }
            self.reply = request.parseJsonRespone(data: data!)!
            
            //            names = reply.map { $0["name"] }
            print(self.reply[0]["name"]!)
            for rep in self.reply {
                self.exList.append(rep["name"]! as! String)
            }
            DispatchQueue.main.async {
                self.exPicker.delegate = self
                self.exPicker.dataSource = self
            }
            
        }.resume()
        
        
        // Do any additional setup after loading the view.
    }
    
    
    
    func numberOfComponents(in pickerView: UIPickerView) -> Int {
        return 1
    }
    
    func pickerView(_ pickerView: UIPickerView, numberOfRowsInComponent component: Int) -> Int {
        return exList.count
    }
    
    func pickerView(_ pickerView: UIPickerView, titleForRow row: Int, forComponent component: Int) -> String? {
        return exList[row]
    }
    
    @IBAction func beginExercise(_ sender: Any) {
        if(!reply.isEmpty) {
            exerciseInfo = reply[exPicker.selectedRow(inComponent: 0)]
            self.performSegue(withIdentifier: "toExercise", sender: self)
        } else {
            return
        }
        print(exerciseInfo)
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
    
}
