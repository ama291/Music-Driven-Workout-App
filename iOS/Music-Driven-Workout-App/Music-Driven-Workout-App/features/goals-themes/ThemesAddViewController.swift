//
//  ThemesAddViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Christopher Choy on 2/25/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit

class ThemesAddViewController: UIViewController {
    
    var userid: String! = "21"
    
    let request = APIRequest()
    var themeName: String! = "theme1"
    var theme: String! = "Artist"
    var numWorkouts: Int = 5
    var reply: String?
    var themeDict: [String:Any] = [:]
    
    @IBOutlet weak var numWorkoutsLabel: UILabel!
    @IBOutlet weak var themeNameTextField: UITextField!
    @IBOutlet weak var spotifySearchbar: UITextField!
    @IBOutlet weak var numLabel: UILabel!
    
    @IBAction func saveTheme(_ sender: Any) {
        self.themeName = self.themeNameTextField.text
        self.theme = self.spotifySearchbar.text
        let qstr = "userid=\(userid!)&name=\(themeName!)&spotifyId=example-id&theme=\(theme!)&numworkouts=\(numWorkouts)&key=SoftCon2018"
        self.request.submitPostLocal(route: "/api/themes/addtheme/", qstring: qstr) { (data, response, error) -> Void in
            if let error = error {
                fatalError(error.localizedDescription)
            }
            self.reply = self.request.parseJsonInitial(data: data!)
            if self.reply != "0" {
                print("Add theme request failed")
                return
            }
            }.resume()
    }
    
    
    @IBAction func numChanged(_ sender: UISlider) {
        self.numWorkouts = Int(sender.value)
        numLabel.text = "Number of Workouts: " + String(numWorkouts)
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        self.numWorkoutsLabel.text = "Number of Workouts: \(numWorkouts)"
        
        // Do any additional setup after loading the view.
    }
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
        if segue.destination is ThemesMenuViewController
        {
            let vc = segue.destination as? ThemesMenuViewController
            vc?.userid = userid
            self.themeDict = ["name": self.themeName, "theme": self.theme, "numWorkouts": self.numWorkouts]
            vc?.themes.append(self.themeDict)
        }
    }
    
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    @IBAction func goBackToThemesMenu(_ sender: UIButton) {
        let storyboard = UIStoryboard(name: "goals-themes", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "themesID") as! ThemesMenuViewController
        vc.userid = userid!
        present(vc, animated: true, completion: nil)
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


