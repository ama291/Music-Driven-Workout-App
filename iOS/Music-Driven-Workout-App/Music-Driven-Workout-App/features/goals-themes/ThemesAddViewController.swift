//
//  ThemesAddViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Christopher Choy on 2/25/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit

struct jsonRequest: Codable {
    var Result: String
    var Status: String
}

class ThemesAddViewController: UIViewController {
    
    var userid: String!
    var themename: String!
    var theme: String!
    var spotifyId: String!
    var numworkouts: String!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
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

    @objc func addThemeAPI() {
        guard let url = URL(string: "http://138.197.49.155:8000/api/themes/addtheme/") else { return }
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        //userid, themename, spotifyId, theme, numworkouts, key
        let postString = "userid=" + userid + "&themename=" + themename
        let postString2 = postString + "&spotifyId=" + spotifyId + "&theme=" + theme + "&numworkouts=" + numworkouts + "&key=SoftCon2018"
        request.httpBody = postString2.data(using: String.Encoding.utf8)
        let session = URLSession.shared
        session.dataTask(with: request) { (data, response, error) in
            if let data = data {
                guard let json = try? JSONDecoder().decode(jsonRequest.self, from: data) else { return }
                self.userid = json.Result
                print(self.userid)
            }

        }.resume()
    }
    
    @IBAction func goToThemeHomeUpdateThemes(_ sender: UIButton) {
        let storyboard = UIStoryboard(name: "goals-themes", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "themesID") as! ThemesMenuViewController
        vc.userid = userid!
        addThemeAPI()
        present(vc, animated: true, completion: nil)
    }
}
